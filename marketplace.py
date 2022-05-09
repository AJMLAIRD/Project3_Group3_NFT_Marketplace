#NFT Marketplace
#Imports
import os
import streamlit as st
from thirdweb import ThirdwebSDK
from eth_account import Account
from dotenv import load_dotenv
from web3 import Web3

from thirdweb.types.nft import NFTMetadataInput

##########################################################################################
# Setup
#load_dotenv()
#key = os.environ.get("PRIVATE_KEY")
provider = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/491b1fe994db42e0b9930eabf7bc6f4c" ))
signer = Account.from_key("PRIVATE KEY")
sdk = ThirdwebSDK(provider, signer)

marketplace = sdk.get_marketplace("0xfC6574220bb22841a23AAd31399f51F4DdA53185")
nft = sdk.get_nft_collection("0x41D8e0C02B595ac2F364dd95C1D763b966dc91DA")

##########################################################################################
pages = ['All Listings', 'Owned Listings', 'Create Listing']
sidebar = st.sidebar.selectbox('Page', pages)

def buyNFT(id):
    marketplace.buyout_listing(id, 1)



##########################################################################################
#All Listings
if sidebar == pages[0]:
    st.header("All Listings")
    listings = marketplace.get_active_listings()
    for i in listings:
        st.text(i.asset.name)
        st.text(i.asset.description)
        st.image(i.asset.image)
        st.text(f"Seller: {i.seller_address}")
        st.text(f"Price: {i.buyout_currency_value_per_token.display_value} {i.buyout_currency_value_per_token.symbol}")
        if st.button("Buy", key=i):
            buyNFT(i.id)

##########################################################################################
#Owned NFTS
if sidebar == pages[1]:
    st.header("Owned NFTs")
    nfts = nft.get_owned("0x92dfA7e486071Bb3B6D6423bBE3817CF8E8af13E")
    print(nfts)

##########################################################################################
#Create
# You can customize this metadata however you like
if sidebar == pages[2]:
    st.header("Create NFT")
    st.file_uploader('Upload a CSV')

    '''
    metadatas = [
        NFTMetadataInput.from_json({
            "name": "Cool NFT",
            "description": "This is a cool NFT",
            "image": open("path/to/file.jpg", "rb"),
        }),
        NFTMetadataInput.from_json({
            "name": "Cooler NFT",
            "description": "This is a cooler NFT",
            "image": open("path/to/file.jpg", "rb"),
        }),
    ]

    # You can pass in any address here to mint the NFT to
    txs = nft.mint_batch_to("0x92dfA7e486071Bb3B6D6423bBE3817CF8E8af13E", metadatas)
    receipt = txs[0].receipt
    first_token_id = txs[0].id
    first_nft = txs[0].data()
    '''
##########################################################################################
#Buy NFT
