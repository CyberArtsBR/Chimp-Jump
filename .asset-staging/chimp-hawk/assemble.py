from pathlib import Path
import base64
import hashlib
import struct

folder = Path('.asset-staging/chimp-hawk')
parts = sorted(folder.glob('part-*.b64'))
assert len(parts) == 18, f'Expected 18 chunks, found {len(parts)}'
encoded = b''.join(chunk.read_bytes() for chunk in parts)
image = base64.b64decode(encoded, validate=True)
assert len(image) == 3437956, 'PNG byte length mismatch'
assert hashlib.sha256(image).hexdigest() == 'ec6ecbc8561b49898ac304d0385895a127c490378a261053da8dae011396714e', 'Original image checksum mismatch'
assert image.startswith(b'\x89PNG\r\n\x1a\n'), 'PNG signature mismatch'
assert struct.unpack('>II', image[16:24]) == (1586, 992), 'PNG dimensions mismatch'
out = Path('public/launcher/cartridge-chimp-hawk-underground.png')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(image)
print(f'Wrote original transparent PNG without modification: {out}, {len(image)} bytes')
