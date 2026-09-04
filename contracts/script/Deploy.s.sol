// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script} from "forge-std/Script.sol";
import {Saeculum} from "../Saeculum.sol";
import {SaeculumOracle} from "../SaeculumOracle.sol";

/// Testnet deploy (docs/DEPLOY_TESTNET.md is the runbook). Reads the
/// initial supply and attestor set from env so the script itself stays
/// committed and generic. NOT for mainnet until the audit closes.
contract Deploy is Script {
    function run() external {
        uint256 initialSupply = vm.envUint("SAEC_INITIAL_SUPPLY"); // archived S in 1e-9 LY
        address[] memory attestors = vm.envAddress("SAEC_ATTESTORS", ",");
        uint256 threshold = vm.envUint("SAEC_THRESHOLD");

        vm.startBroadcast();
        address deployer = msg.sender;
        uint64 nonce = vm.getNonce(deployer);
        address predictedOracle = vm.computeCreateAddress(deployer, nonce + 1);
        Saeculum token = new Saeculum(initialSupply, predictedOracle);
        SaeculumOracle oracle = new SaeculumOracle(token, attestors, threshold);
        require(address(oracle) == predictedOracle, "nonce drift");
        vm.stopBroadcast();
    }
}
