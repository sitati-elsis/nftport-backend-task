import os

from . import db, ma
from sqlalchemy.dialects.postgresql import JSONB


class Contract(db.Model):
    __tablename__ = 'contracts'
    symbol = db.Column(db.String(255), nullable=False, primary_key=True)
    contract_address = db.Column(db.String(255), nullable=False, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=True)


class Nft(db.Model):
    __tablename__ = 'nfts'
    token_id = db.Column(db.String(255), nullable=False, primary_key=True)
    contract_address = db.Column(db.String(255), nullable=False,  primary_key=True)
    chain = db.Column(db.String(255), nullable=False)
    image = db.Column(db.Text, nullable=True)
    token_uri = db.Column(db.String(255), nullable=True)
    attributes = db.Column(JSONB, nullable=True)

    @property
    def image_url(self):
        return os.path.join(os.getenv('ASSETS_URL', "http://127.0.0.1:5000/"), f"{os.path.basename(self.image)}.png", )


class NftSchema(ma.Schema):
    class Meta:
        fields = ("token_id", "contract_address", "chain", "image", "token_uri", "attributes", "image_url")
        model = Nft