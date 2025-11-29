from array import array
import moderngl as mgl

""" from scripts.datablock import Datablock """
from scripts.core.settings import DEFAULT_SHADER_PATH

class OGLHandler:
    def __init__(self, appInstance):
        self.app = appInstance

    def OGL_init(self):

        # prepare modernGL prerequisities
        self.ctx = mgl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array("f", [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0,
        ]))

        self.create_gl_program()

    def create_gl_program(self):
        self.load_shaders()
        self.program = self.ctx.program(vertex_shader=self.vertex, fragment_shader=self.fragment)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def surf_to_tex(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (mgl.NEAREST, mgl.NEAREST)
        tex.swizzle = "BGRA"
        tex.write(surf.get_view("1"))

        return tex

    def load_shaders(self, pathToFiles:tuple=DEFAULT_SHADER_PATH):
        with open(pathToFiles + ".vert", 'r') as f:
            self.vertex = f.read()
        with open(pathToFiles + ".frag", 'r') as f:
            self.fragment = f.read()
