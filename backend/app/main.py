import os
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.infrastructure.database.database import init_db
from app.infrastructure.database.repositories import MongoUserRepository, MongoAgreementRepository
from app.infrastructure.blockchain.monad_client import MonadBlockChainService, load_contract_abi

from app.application.use_case.create_user import CreateUserUseCase
from app.application.use_case.sign_agreement import SignAgreementUseCase
from app.application.use_case.create_agreement import CreateAgreementUseCase
from app.application.use_case.get_agreement import GetAgreementUseCase

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    #startup 
    
    user_repository = MongoUserRepository()
    agreement_repository = MongoAgreementRepository()
    blockchain_service = MonadBlockChainService(
        monad_rpc_url = os.getenv("MONAD_RPC_URL"),
        contract_address = os.getenv("CONTRACT_ADDRESS"),
        contract_abi = load_contract_abi(),
        chain_id = int(os.getenv("CHAIN_ID"))
    )
    
    app.state.create_user_use_case = CreateUserUseCase(user_repository)
    app.state.create_agreement_use_case = CreateAgreementUseCase(agreement_repository, user_repository)
    app.state.sign_agreement_use_case = SignAgreementUseCase(agreement_repository, user_repository, blockchain_service)
    app.state.get_agreement_use_case = GetAgreementUseCase(agreement_repository)
    
    yield 
app = FastAPI(title="ProofVault", lifespan = lifespan)
@app.get("/")
async def root():
    return{"message": "ProofVault API is running successfully!"}