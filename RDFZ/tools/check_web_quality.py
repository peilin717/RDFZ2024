"""Verify full-size WebP dimensions, lossless alpha and visible luminance SSIM.
Requires Pillow, numpy and scipy. Prints a JSON report.
"""
from pathlib import Path
from PIL import Image
from scipy.ndimage import uniform_filter
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import json
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'asset-manifest.js').read_text().split(' = ',1)[1].rstrip(';\n'))
def compare(item):
 source,variants=item
 original=Image.open(root/source).convert('RGBA')
 encoded=Image.open(root/variants['full']).convert('RGBA')
 assert original.size==encoded.size,source
 a=np.array(original);b=np.array(encoded)
 assert np.array_equal(a[:,:,3],b[:,:,3]),source
 # Compare visible luminance composited over the game's dark background.
 def luminance(pixels):
  alpha=pixels[:,:,3].astype(np.float32)/255
  return (pixels[:,:,:3].astype(np.float32) @ np.array([.299,.587,.114],dtype=np.float32))*alpha+12*(1-alpha)
 x,y=luminance(a),luminance(b)
 ux,uy=uniform_filter(x,11),uniform_filter(y,11)
 vx=uniform_filter(x*x,11)-ux*ux;vy=uniform_filter(y*y,11)-uy*uy
 cov=uniform_filter(x*y,11)-ux*uy
 ssim=((2*ux*uy+6.5025)*(2*cov+58.5225))/((ux*ux+uy*uy+6.5025)*(vx+vy+58.5225))
 return {'source':source,'ssim':float(ssim[5:-5,5:-5].mean()),'original_bytes':(root/source).stat().st_size,'webp_bytes':(root/variants['full']).stat().st_size}
with ThreadPoolExecutor(max_workers=2) as pool:
 rows=list(pool.map(compare,manifest.items()))
print(json.dumps({'count':len(rows),'mean_ssim':float(np.mean([r['ssim'] for r in rows])),'min_ssim':min(r['ssim'] for r in rows),'worst':sorted(rows,key=lambda r:r['ssim'])[:5],'full_original_bytes':sum(r['original_bytes'] for r in rows),'full_webp_bytes':sum(r['webp_bytes'] for r in rows),'dimensions_preserved':True,'alpha_exact':True},indent=2))
