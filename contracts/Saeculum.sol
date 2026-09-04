// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title SAECULUM — the rebasing claim on humanity's remaining time
/// @notice REFERENCE IMPLEMENTATION (S-05, pre-audit artifact). This
///   contract is the Solidity rendering of the tested Python spec
///   (tly/gons.py + tly/token_model.py — the property tests there are
///   normative). NOT DEPLOYED, NOT AUDITED. Do not use before the P6
///   audits and counsel sign-off.
///
/// Design (SPEC capability 5; DECISIONS kappa = 1 token per life-year):
/// - Internally every wallet holds GONS: fixed integers that never
///   change on a rebase. TOTAL_GONS = 10^30.
/// - The public balance is gons / F where F = TOTAL_GONS / M and M is
///   the current supply = S(t) * 10^DECIMALS quanta. A weekly oracle
///   rebase sets M to the archived print's S — balances scale, SHARES
///   never move (share invariance, the audited property).
/// - The oracle is the weekly SETTLEMENT print: epoch, S, and the
///   archive record hash. Anyone can verify the hash against the
///   public archive chain; an N-of-M attestation (P5's external
///   recomputers) gates acceptance.
contract Saeculum {
    string public constant name = "Saeculum";
    string public constant symbol = "SAEC";
    uint8 public constant decimals = 9; // 1 token = 1 life-year; 1e-9 granularity

    uint256 private constant TOTAL_GONS = 10 ** 30;
    uint256 public totalSupply; // in 1e-9 life-year quanta

    mapping(address => uint256) private _gons;
    mapping(address => mapping(address => uint256)) private _allowedFragments;

    // --- oracle state ---
    // Mutable BY DESIGN (slither immutable-states finding reviewed and
    // rejected): succession must be possible — only the CURRENT oracle
    // can hand over, and the N-of-M oracle contract requires threshold
    // attestation of the successor address (SaeculumOracle.attestHandover).
    address public oracle;
    bytes32 public lastRecordHash; // archive chain record_hash of the last rebase
    uint64 public lastEpoch; // unix time of the Monday 12:00 UTC epoch

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Rebase(uint64 indexed epoch, uint256 oldSupply, uint256 newSupply, bytes32 recordHash);
    event OracleHandover(address indexed oldOracle, address indexed newOracle);

    error NotOracle();
    error EpochNotMonotonic();
    error ZeroSupply();
    error ZeroAddress();

    constructor(uint256 initialSupply, address oracle_) {
        if (initialSupply == 0) revert ZeroSupply();
        if (oracle_ == address(0)) revert ZeroAddress(); // a zero oracle bricks rebases forever
        totalSupply = initialSupply;
        oracle = oracle_;
        _gons[msg.sender] = TOTAL_GONS;
        emit Transfer(address(0), msg.sender, initialSupply);
    }

    /// @dev Multiply-then-divide, never a floored gons-per-fragment:
    ///   the property tests caught the AMPL-style form
    ///   (gons / floor(TOTAL_GONS / supply)) letting the SUM of
    ///   balances exceed totalSupply; this form guarantees
    ///   sum(balances) <= totalSupply always. No overflow: gons <=
    ///   1e30 and supply < 1e21 quanta, so the product < 1e51 << 2^256.
    ///   Transfers ceil the gon cost (sender absorbs rounding), so a
    ///   transfer can never deliver more than it debits.
    function balanceOf(address who) public view returns (uint256) {
        return (_gons[who] * totalSupply) / TOTAL_GONS;
    }

    /// @notice Weekly settlement rebase. New supply = the archived
    ///   print's S in 1e-9 quanta. Gons are UNTOUCHED: every holder's
    ///   share of TOTAL_GONS — and therefore of humanity's remaining
    ///   time — is exactly what it was the block before.
    function rebase(uint64 epoch, uint256 newSupply, bytes32 recordHash) external {
        if (msg.sender != oracle) revert NotOracle();
        if (epoch <= lastEpoch) revert EpochNotMonotonic(); // first print settles
        if (newSupply == 0) revert ZeroSupply();
        uint256 old = totalSupply;
        totalSupply = newSupply;
        lastEpoch = epoch;
        lastRecordHash = recordHash;
        emit Rebase(epoch, old, newSupply, recordHash);
    }

    /// @notice Oracle succession — callable only by the current oracle
    ///   (which, being the N-of-M contract, itself requires threshold
    ///   attestation to invoke this).
    function setOracle(address newOracle) external {
        if (msg.sender != oracle) revert NotOracle();
        if (newOracle == address(0)) revert ZeroAddress();
        emit OracleHandover(oracle, newOracle);
        oracle = newOracle;
    }

    function transfer(address to, uint256 value) external returns (bool) {
        // gons fixed at transfer time only (tly/gons.py rule); ceil the
        // gon cost so the SENDER absorbs rounding — a transfer can never
        // deliver more balance than it debits.
        uint256 gonValue = (value * TOTAL_GONS + totalSupply - 1) / totalSupply;
        _gons[msg.sender] -= gonValue;
        _gons[to] += gonValue;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function allowance(address owner_, address spender) external view returns (uint256) {
        return _allowedFragments[owner_][spender];
    }

    function approve(address spender, uint256 value) external returns (bool) {
        _allowedFragments[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        _allowedFragments[from][msg.sender] -= value;
        uint256 gonValue = (value * TOTAL_GONS + totalSupply - 1) / totalSupply;
        _gons[from] -= gonValue;
        _gons[to] += gonValue;
        emit Transfer(from, to, value);
        return true;
    }
}
