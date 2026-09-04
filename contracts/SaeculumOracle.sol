// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Saeculum} from "./Saeculum.sol";

/// @title SaeculumOracle — N-of-M attested settlement rebases
/// @notice REFERENCE IMPLEMENTATION (pre-audit). The launch oracle:
///   the token's single `oracle` address is THIS contract, and a rebase
///   executes only when >= threshold independent attestors have
///   submitted byte-identical (epoch, supply, recordHash) tuples —
///   the on-chain form of P5's N-of-M external-recomputer rule. Every
///   attestor independently recomputes the weekly print from public
///   artifacts (docs/REPRODUCE_FIXING.md) and attests what THEY
///   computed; agreement is the settlement.
///
/// Deliberately absent (scope honesty): attestor slashing/rotation
///   economics (P6 governance decides them); disagreement here simply
///   stalls the rebase — the failure ladder's DEFER, on-chain. A
///   stalled epoch is skippable: attestation keys to the epoch, and a
///   later epoch can settle while an earlier one never reached
///   threshold (first print settles; a missed fixing stays missed).
contract SaeculumOracle {
    Saeculum public immutable token;
    uint256 public immutable threshold; // N
    address[] public attestors; // M

    // epoch => attestor => attestation hash (keccak of the tuple)
    mapping(uint64 => mapping(address => bytes32)) public attestations;
    // epoch => attestation hash => count
    mapping(uint64 => mapping(bytes32 => uint256)) public tallies;
    mapping(address => bool) public isAttestor;

    event Attested(uint64 indexed epoch, address indexed attestor, bytes32 tupleHash);
    event Settled(uint64 indexed epoch, uint256 supply, bytes32 recordHash, uint256 tally);
    event HandoverAttested(address indexed attestor, address indexed successor);
    event HandedOver(address indexed successor, uint256 tally);

    error NotAttestor();
    error BadThreshold();
    error AlreadySettledEpoch();

    constructor(Saeculum token_, address[] memory attestors_, uint256 threshold_) {
        if (threshold_ == 0 || threshold_ > attestors_.length) revert BadThreshold();
        token = token_;
        attestors = attestors_;
        threshold = threshold_;
        for (uint256 i = 0; i < attestors_.length; i++) {
            isAttestor[attestors_[i]] = true;
        }
    }

    /// @notice Attest the settlement tuple you independently recomputed.
    ///   Re-attesting the same epoch REPLACES your previous attestation
    ///   (a recomputer that finds its own error may correct itself until
    ///   the epoch settles); once threshold is reached the rebase fires
    ///   and the token's monotonic-epoch rule makes the epoch final.
    function attest(uint64 epoch, uint256 supply, bytes32 recordHash) external {
        if (!isAttestor[msg.sender]) revert NotAttestor();
        if (epoch <= token.lastEpoch()) revert AlreadySettledEpoch();
        bytes32 tupleHash = keccak256(abi.encode(epoch, supply, recordHash));
        bytes32 prev = attestations[epoch][msg.sender];
        if (prev == tupleHash) return; // idempotent
        if (prev != bytes32(0)) tallies[epoch][prev] -= 1; // replace
        attestations[epoch][msg.sender] = tupleHash;
        tallies[epoch][tupleHash] += 1;
        emit Attested(epoch, msg.sender, tupleHash);
        if (tallies[epoch][tupleHash] >= threshold) {
            token.rebase(epoch, supply, recordHash);
            emit Settled(epoch, supply, recordHash, tallies[epoch][tupleHash]);
        }
    }

    // successor => attestor => attested?
    mapping(address => mapping(address => bool)) public handoverAttested;
    mapping(address => uint256) public handoverTally;

    /// @notice Attest a SUCCESSOR oracle contract (attestor-set rotation
    ///   happens by deploying a new oracle and migrating via threshold
    ///   agreement here). Reaching threshold calls token.setOracle —
    ///   after which THIS contract is inert.
    function attestHandover(address successor) external {
        if (!isAttestor[msg.sender]) revert NotAttestor();
        if (handoverAttested[successor][msg.sender]) return; // idempotent
        handoverAttested[successor][msg.sender] = true;
        handoverTally[successor] += 1;
        emit HandoverAttested(msg.sender, successor);
        if (handoverTally[successor] >= threshold) {
            token.setOracle(successor);
            emit HandedOver(successor, handoverTally[successor]);
        }
    }

    function attestorCount() external view returns (uint256) {
        return attestors.length;
    }
}
