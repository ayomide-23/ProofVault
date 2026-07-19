// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract ProofVault {
    struct Agreement {
        bytes32 termsHash;
        address creator;
        address counterparty;
        uint256 timestamp;
    }

    mapping(uint256 => Agreement) public agreements;
    uint256 public agreementCount;

    event AgreementRecorded(
        uint256 indexed id,
        bytes32 termsHash,
        address indexed creator,
        address indexed counterparty,
        uint256 timestamp
    );

    function recordAgreement(
        bytes32 termsHash,
        address creator,
        address counterparty
    ) external returns (uint256) {
        require(msg.sender == counterparty, "Only counterparty can confirm");

        agreementCount++;
        uint256 id = agreementCount;

        agreements[id] = Agreement({
            termsHash: termsHash,
            creator: creator,
            counterparty: counterparty,
            timestamp: block.timestamp
        });

        emit AgreementRecorded(id, termsHash, creator, counterparty, block.timestamp);
        return id;
    }

    function getAgreement(uint256 id) external view returns (
        bytes32 termsHash,
        address creator,
        address counterparty,
        uint256 timestamp
    ) {
        Agreement memory a = agreements[id];
        return (a.termsHash, a.creator, a.counterparty, a.timestamp);
    }
}