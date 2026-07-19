import {network} from "hardhat";

async function main(){
    const { viem } = await network.connect() //connecting to the blockchain
    const proofvault = await viem.deployContract("ProofVault") //deploying the contract

    console.log("ProofVault contract deployed to:", proofvault.address) //logging the contract address
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});