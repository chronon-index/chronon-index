// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {Saeculum} from "../Saeculum.sol";

/// S-10 audit-prep: the executable form of docs/audit/SECURITY_PROPERTIES.md.
/// Mirrors tests/test_token_model.py (the Python normative model) — a
/// divergence between the three artifacts is itself a finding.
contract SaeculumTest is Test {
    uint256 constant S0 = 362_412_641_743 * 1e9;
    uint256 constant S1 = 363_511_706_093 * 1e9;
    uint256 constant TOTAL_GONS = 10 ** 30;

    Saeculum token;
    address oracle = address(0x0AC1E);
    address alice = address(0xA11CE);
    address bob = address(0xB0B);

    function setUp() public {
        token = new Saeculum(S0, oracle);
        token.transfer(alice, 1_000_000 * 1e9);
        token.transfer(bob, 250_000 * 1e9);
    }

    /// P-share: rebase moves no one's share (checked via balance ratio
    /// against a reference wallet staying constant to 1 part in 1e12).
    function testFuzz_ShareInvarianceUnderRebase(uint256 newSupply) public {
        newSupply = bound(newSupply, S0 / 100, S0 * 100);
        uint256 aBefore = token.balanceOf(alice);
        uint256 tBefore = token.totalSupply();
        vm.prank(oracle);
        token.rebase(1, newSupply, bytes32(uint256(1)));
        // share = balance/supply is preserved across the rebase
        assertApproxEqRel(
            token.balanceOf(alice) * 1e18 / token.totalSupply(),
            aBefore * 1e18 / tBefore,
            1e6 // 1 part in 1e12
        );
    }

    /// P-mortality-neutrality: any rebase path to the same S ends equal.
    function testFuzz_PathIndependence(uint256 mid1, uint256 mid2) public {
        mid1 = bound(mid1, S0 / 10, S0 * 10);
        mid2 = bound(mid2, S0 / 10, S0 * 10);
        Saeculum b = new Saeculum(S0, oracle);
        b.transfer(alice, 1_000_000 * 1e9);
        b.transfer(bob, 250_000 * 1e9);
        vm.startPrank(oracle);
        token.rebase(1, mid1, 0);
        token.rebase(2, mid2, 0);
        token.rebase(3, S1, 0);
        b.rebase(1, S1, 0);
        vm.stopPrank();
        assertEq(token.balanceOf(alice), b.balanceOf(alice));
        assertEq(token.balanceOf(bob), b.balanceOf(bob));
    }

    /// P-conservation: sum(balances) can never exceed totalSupply, and a
    /// transfer can never increase the recipient by more than it debits.
    function testFuzz_TransferNeverMints(uint96 value, uint256 newSupply) public {
        newSupply = bound(newSupply, S0 / 100, S0 * 100);
        vm.prank(oracle);
        token.rebase(1, newSupply, 0);
        uint256 v = bound(uint256(value), 0, token.balanceOf(alice));
        uint256 sumBefore = token.balanceOf(alice) + token.balanceOf(bob);
        vm.prank(alice);
        token.transfer(bob, v);
        assertLe(token.balanceOf(alice) + token.balanceOf(bob), sumBefore);
        assertLe(
            token.balanceOf(address(this)) + token.balanceOf(alice) + token.balanceOf(bob),
            token.totalSupply()
        );
    }

    /// P-monotonic-epoch: replay/reorder reverts; non-oracle reverts.
    function test_FirstPrintSettlesOnChain() public {
        vm.prank(oracle);
        token.rebase(10, S1, 0);
        vm.prank(oracle);
        vm.expectRevert(Saeculum.EpochNotMonotonic.selector);
        token.rebase(10, S0, 0);
        vm.prank(oracle);
        vm.expectRevert(Saeculum.EpochNotMonotonic.selector);
        token.rebase(9, S0, 0);
        vm.expectRevert(Saeculum.NotOracle.selector);
        token.rebase(11, S0 / 2, 0);
    }

    /// Parity with the Python model on a fixed operation sequence.
    function test_ParityWithNormativeModel() public {
        vm.prank(oracle);
        token.rebase(1, S1, 0);
        vm.prank(alice);
        token.transfer(bob, 7_777_777);
        // expected values computed by tly/token_model.py (committed in
        // docs/audit/SECURITY_PROPERTIES.md; regenerate with
        // tly.token_model on the same op sequence if it changes)
        assertEq(token.balanceOf(alice), 1003032624706327);
        assertEq(token.balanceOf(bob), 250758165898803);
    }
}
