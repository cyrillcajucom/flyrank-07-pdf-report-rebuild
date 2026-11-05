from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
root=Path(__file__).parent
pages=[Image.open(p).convert('RGB') for p in sorted(root.glob('review-page-*.png'))]
w,h=pages[0].size
sheet=Image.new('RGB',(w*4,h*2),'#cccccc')
for i,p in enumerate(pages):sheet.paste(p,((i%4)*w,(i//4)*h))
sheet.save(root/'all-pages-review.png')
