// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {Saeculum} from "../Saeculum.sol";
import {SaeculumOracle} from "../SaeculumOracle.sol";

contract SaeculumOracleTest is Test {
    uint256 constant S0 = 362_412_641_743 * 1e9;
    uint256 constant S1 = 363_511_706_093 * 1e9;

    Saeculum token;
    SaeculumOracle oracle;
    address a1 = address(0xA1);
    address a2 = address(0xA2);
    address a3 = address(0xA3);
    address outsider = address(0xBAD);

    function setUp() public {
        // deploy token with a placeholder oracle, then hand over: the
        // constructor needs the token address and vice versa, so the
        // token's oracle is set to the CONTRACT WE PRE-COMPUTE via
        // deterministic deployment order (nonce arithmetic in tests:
        // deploy token with computed oracle address).
        address predicted = vm.computeCreateAddress(address(this), vm.getNonce(address(this)) + 1);
        token = new Saeculum(S0, predicted);
        address[] memory att = new address[](3);
        att[0] = a1;
        att[1] = a2;
        att[2] = a3;
        oracle = new SaeculumOracle(token, att, 2);
        assertEq(address(oracle), predicted);
    }

    function test_2of3_settles_and_third_is_noop() public {
        vm.prank(a1);
        oracle.attest(1, S1, bytes32(uint256(0xABC)));
        assertEq(token.totalSupply(), S0); // 1 of 2 — not yet
        vm.prank(a2);
        oracle.attest(1, S1, bytes32(uint256(0xABC)));
        assertEq(token.totalSupply(), S1); // settled
        assertEq(token.lastEpoch(), 1);
        vm.prank(a3);
        vm.expectRevert(SaeculumOracle.AlreadySettledEpoch.selector);
        oracle.attest(1, S1, bytes32(uint256(0xABC)));
    }

    function test_disagreement_stalls_never_settles_wrong_value() public {
        vm.prank(a1);
        oracle.attest(1, S1, bytes32(uint256(1)));
        vm.prank(a2);
        oracle.attest(1, S1 + 1, bytes32(uint256(1))); // divergent recompute
        assertEq(token.totalSupply(), S0); // stalled: no 2 agree
        // a3 breaks the tie with the correct tuple
        vm.prank(a3);
        oracle.attest(1, S1, bytes32(uint256(1)));
        assertEq(token.totalSupply(), S1);
    }

    function test_self_correction_replaces_attestation() public {
        vm.prank(a1);
        oracle.attest(1, S1 + 999, bytes32(uint256(1))); // a1 errs
        vm.prank(a1);
        oracle.attest(1, S1, bytes32(uint256(1))); // a1 corrects itself
        assertEq(oracle.tallies(1, keccak256(abi.encode(uint64(1), S1 + 999, bytes32(uint256(1))))), 0);
        vm.prank(a2);
        oracle.attest(1, S1, bytes32(uint256(1)));
        assertEq(token.totalSupply(), S1);
    }

    function test_outsider_and_skipped_epoch() public {
        vm.prank(outsider);
        vm.expectRevert(SaeculumOracle.NotAttestor.selector);
        oracle.attest(1, S1, 0);
        // epoch 1 never reaches threshold; epoch 2 settles over it
        vm.prank(a1);
        oracle.attest(1, S1, 0);
        vm.prank(a1);
        oracle.attest(2, S1, bytes32(uint256(2)));
        vm.prank(a2);
        oracle.attest(2, S1, bytes32(uint256(2)));
        assertEq(token.lastEpoch(), 2); // missed fixing stays missed
        vm.prank(a3);
        vm.expectRevert(SaeculumOracle.AlreadySettledEpoch.selector);
        oracle.attest(1, S1, 0);
    }

    function testFuzz_threshold_boundary(uint8 nAgree) public {
        uint256 agree = bound(uint256(nAgree), 0, 3);
        address[3] memory att = [a1, a2, a3];
        for (uint256 i = 0; i < agree; i++) {
            if (token.lastEpoch() >= 1) break; // settled: further attests revert by design
            vm.prank(att[i]);
            oracle.attest(1, S1, bytes32(uint256(7)));
        }
        if (agree >= 2) assertEq(token.totalSupply(), S1);
        else assertEq(token.totalSupply(), S0);
    }
}
