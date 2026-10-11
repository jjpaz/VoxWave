"""Checks for SVG interpretation and audio-driven animation; no API calls."""
import array
import unittest
from render_brand_transition import parse_path, load_geometry, envelope, RATE


class BrandTransitionTests(unittest.TestCase):
    def test_relative_move_after_closed_subpath(self):
        rings=parse_path('M10 20l10 0 0 10-10 0z m2 2l6 0 0 6-6 0z')
        self.assertEqual(rings[0],[(10.,20.),(20.,20.),(20.,30.),(10.,30.)])
        self.assertEqual(rings[1][0],(12.,22.))
        self.assertEqual(rings[1][-1],(12.,28.))

    def test_relative_cubic_endpoint(self):
        points=parse_path('M10 10c0 10 10 10 10 0z')[0]
        self.assertEqual(points[-1],(20.,10.))
        self.assertGreater(max(p[1] for p in points),17)

    def test_canonical_geometry_and_letter_counter(self):
        symbols,letters,sha=load_geometry()
        self.assertEqual(set(symbols),{'navy','teal','coral'})
        self.assertEqual(len(letters),7)
        self.assertEqual(len(sha),64)
        # Second letter is the official 'o': its centre stays transparent.
        mask=letters[1][2]
        self.assertEqual(mask.getpixel((mask.width//2,mask.height//2)),0)
        self.assertGreater(mask.getextrema()[1],0)

    def test_voice_envelope_settles_in_silence(self):
        samples=array.array('h',[0])*(RATE//2)
        samples.extend(array.array('h',[10000])*(RATE//2))
        samples.extend(array.array('h',[0])*(RATE*3))
        values,dt=envelope(samples)
        self.assertEqual(max(values[:40]),0)
        self.assertGreater(max(values),.8)
        self.assertLess(values[-1],.001)
        self.assertAlmostEqual(dt,.01,places=3)


if __name__=='__main__':
    unittest.main()
