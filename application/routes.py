from flask import request, make_response, jsonify
from flask import current_app as app
from .models import Nft, NftSchema
from flask import send_from_directory
import os.path
# Use folder called 'assets' sitting next to app.py module.
assets_folder = os.path.join(app.root_path, 'assets')
@app.route('/api/v1/nfts', methods=['GET'])
def get_contract_nfts():
   contract_address = request.args.get('contract_address')
   get_nfts = Nft.query.filter_by(contract_address=contract_address)
   nft_schema = NftSchema(many=True)
   nfts = nft_schema.dump(get_nfts)
   return make_response(jsonify({"nfts": nfts}))


@app.route('/assets/<path:filename>')
def assets(filename):
  # Add custom handling here.
  # Send a file download response.
  print(assets_folder)
  return send_from_directory(assets_folder, filename)