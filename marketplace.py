#NFT Marketplace
#Imports
import os
from unicodedata import name
import streamlit as st
from thirdweb import ThirdwebSDK
from eth_account import Account
from dotenv import load_dotenv
import json
from web3 import Web3
import PIL  

from thirdweb.types.nft import NFTMetadataInput

##########################################################################################
# Setup
#load_dotenv()
#key = os.environ.get("PRIVATE_KEY")
provider = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/491b1fe994db42e0b9930eabf7bc6f4c" ))
signer = Account.from_key("0xca384b5b7366440effaccfaf72e2d1d0d645e87fe983803f1bdcbc92d2849d11")
sdk = ThirdwebSDK(provider, signer)

marketplace = sdk.get_marketplace("0xfC6574220bb22841a23AAd31399f51F4DdA53185")
nft = sdk.get_nft_collection("0x41D8e0C02B595ac2F364dd95C1D763b966dc91DA")
address = "0x92dfA7e486071Bb3B6D6423bBE3817CF8E8af13E"
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
        if st.button("Buy", key=i.id):
            buyNFT(i.id)

##########################################################################################
#Owned NFTS
if sidebar == pages[1]:
    st.header("Owned NFTs")
    nfts = nft.get_owned(address)
    for i in nfts:
        st.text(i.metadata.name)
        st.text(i.metadata.description)
        st.image(i.metadata.image)
        

##########################################################################################
#Create
# You can customize this metadata however you like
if sidebar == pages[2]:
    st.header("Create NFT")
    image = st.file_uploader('Upload an image')
    if image:
        st.image(image)
    NFTname = st.text_input("Input Name")
    description = st.text_input("Input Description")

    if st.button("Mint"):
    # You can pass in any address here to mint the NFT to
        metadata = NFTMetadataInput.from_json({
                "name": NFTname,
                "description": description,
                "image": {NFTname}.jpg,
            })
        

        
        tx = nft.mint(metadata)
        receipt = tx.receipt
        token_id = tx.id
        nft = tx.data()
        
       