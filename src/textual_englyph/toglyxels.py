from textual.strip import Strip
from rich.console import Console
from rich.segment import Segment
from rich.style import Style
#from rich.traceback import install
#install()
#raise ValueError("My message")

from typing import List
from PIL import Image, ImageDraw, ImageFont
from importlib import resources

class ToGlyxels():
    """Glyph pixels to enable user specified font based string rendering via PIL"""

    #full infill glyxel(glyph pixel) look up table, columns x rows
    full_glut = [[],["","",""],["","","","",""]]
    full_glut[1][1] = " █"
    full_glut[1][2] = " ▀▄█"
    full_glut[2][2] = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"
    full_glut[2][3] = " 🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬑🬒🬓▌🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬧▐🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻█"
    full_glut[2][4] = " 𜺨𜺫🮂𜴀▘𜴁𜴂𜴃𜴄▝𜴅𜴆𜴇𜴈▀𜴉𜴊𜴋𜴌🯦𜴍𜴎𜴏𜴐𜴑𜴒𜴓𜴔𜴕𜴖𜴗𜴘𜴙𜴚𜴛𜴜𜴝𜴞𜴟🯧𜴠𜴡𜴢𜴣𜴤𜴥𜴦𜴧𜴨𜴩𜴪𜴫𜴬𜴭𜴮𜴯𜴰𜴱𜴲𜴳𜴴𜴵🮅𜺣𜴶𜴷𜴸𜴹𜴺𜴻𜴼𜴽𜴾𜴿𜵀𜵁𜵂𜵃𜵄▖𜵅𜵆𜵇𜵈▌𜵉𜵊𜵋𜵌▞𜵍𜵎𜵏𜵐▛𜵑𜵒𜵓𜵔𜵕𜵖𜵗𜵘𜵙𜵚𜵛𜵜𜵝𜵞𜵟𜵠𜵡𜵢𜵣𜵤𜵥𜵦𜵧𜵨𜵩𜵪𜵫𜵬𜵭𜵮𜵯𜵰𜺠𜵱𜵲𜵳𜵴𜵵𜵶𜵷𜵸𜵹𜵺𜵻𜵼𜵽𜵾𜵿𜶀𜶁𜶂𜶃𜶄𜶅𜶆𜶇𜶈𜶉𜶊𜶋𜶌𜶍𜶎𜶏▗𜶐𜶑𜶒𜶓▚𜶔𜶕𜶖𜶗▐𜶘𜶙𜶚𜶛▜𜶜𜶝𜶞𜶟𜶠𜶡𜶢𜶣𜶤𜶥𜶦𜶧𜶨𜶩𜶪𜶫▂𜶬𜶭𜶮𜶯𜶰𜶱𜶲𜶳𜶴𜶵𜶶𜶷𜶸𜶹𜶺𜶻𜶼𜶽𜶾𜶿𜷀𜷁𜷂𜷃𜷄𜷅𜷆𜷇𜷈𜷉𜷊𜷋𜷌𜷍𜷎𜷏𜷐𜷑𜷒𜷓𜷔𜷕𜷖𜷗𜷘𜷙𜷚▄𜷛𜷜𜷝𜷞▙𜷟𜷠𜷡𜷢▟𜷣▆𜷤𜷥█"
    #partial infill pixels(pips) glyxel look up table, columns x rows
    pips_glut =  [[],["","",""],["","","","",""]]
    pips_glut[1][1] = " ●"
    pips_glut[1][2] = " ᛫.:"
    pips_glut[2][2] = " 𜰡𜰢𜰣𜰤𜰥𜰦𜰧𜰨𜰩𜰪𜰫𜰬𜰭𜰮𜰯"
    pips_glut[2][3] = " 𜹑𜹒𜹓𜹔𜹕𜹖𜹗𜹘𜹙𜹚𜹛𜹜𜹝𜹞𜹟𜹠𜹡𜹢𜹣𜹤𜹥𜹦𜹧𜹨𜹩𜹪𜹫𜹬𜹭𜹮𜹯𜹰𜹱𜹲𜹳𜹴𜹵𜹶𜹷𜹸𜹹𜹺𜹻𜹼𜹽𜹾𜹿𜺀𜺁𜺂𜺃𜺄𜺅𜺆𜺇𜺈𜺉𜺊𜺋𜺌𜺍𜺎𜺏"
    pips_glut[2][4] = "⠀⠁⠈⠉⠂⠃⠊⠋⠐⠑⠘⠙⠒⠓⠚⠛⠄⠅⠌⠍⠆⠇⠎⠏⠔⠕⠜⠝⠖⠗⠞⠟⠠⠡⠨⠩⠢⠣⠪⠫⠰⠱⠸⠹⠲⠳⠺⠻⠤⠥⠬⠭⠦⠧⠮⠯⠴⠵⠼⠽⠶⠷⠾⠿⡀⡁⡈⡉⡂⡃⡊⡋⡐⡑⡘⡙⡒⡓⡚⡛⡄⡅⡌⡍⡆⡇⡎⡏⡔⡕⡜⡝⡖⡗⡞⡟⡠⡡⡨⡩⡢⡣⡪⡫⡰⡱⡸⡹⡲⡳⡺⡻⡤⡥⡬⡭⡦⡧⡮⡯⡴⡵⡼⡽⡶⡷⡾⡿⢀⢁⢈⢉⢂⢃⢊⢋⢐⢑⢘⢙⢒⢓⢚⢛⢄⢅⢌⢍⢆⢇⢎⢏⢔⢕⢜⢝⢖⢗⢞⢟⢠⢡⢨⢩⢢⢣⢪⢫⢰⢱⢸⢹⢲⢳⢺⢻⢤⢥⢬⢭⢦⢧⢮⢯⢴⢵⢼⢽⢶⢷⢾⢿⣀⣁⣈⣉⣂⣃⣊⣋⣐⣑⣘⣙⣒⣓⣚⣛⣄⣅⣌⣍⣆⣇⣎⣏⣔⣕⣜⣝⣖⣗⣞⣟⣠⣡⣨⣩⣢⣣⣪⣫⣰⣱⣸⣹⣲⣳⣺⣻⣤⣥⣬⣭⣦⣧⣮⣯⣴⣵⣼⣽⣶⣷⣾⣿"


    @staticmethod
    def pane2strips(
            style: Style|None,
            basis,
            pane,
            pips ) -> List[List[Segment]]:
        x,y,mask = pane
        if x == 0 or y == 0: return [ Strip.blank(0) ]

        glut = ToGlyxels.pips_glut if pips else ToGlyxels.full_glut

        selection = Image.new( '1', (x,y) )
        selection.putdata(mask)
        #glyph based pixels must be an integer multiple of glyph cell basis, ie. 2x4 -> octants
        while x % basis[0] != 0: x += 1
        while y % basis[1] != 0: y += 1
        slate = Image.new( '1', (x,y) )
        #place bitmap into upper left corner
        slate.paste( selection, (0,0) )

        strips = []
        for y_glyph in range( 0, y, basis[1] ):
            y_strip = []
            for x_glyph in range( 0, x, basis[0] ):
                glyph_idx = 0
                glyxelList = []
                for y_idx in range( basis[1] ):
                    for x_idx in range( basis[0] ):
                        glyxelList.append( slate.getpixel( (x_glyph+x_idx, y_glyph+y_idx) ) )
                for exp, gColor in enumerate( glyxelList ):
                    if gColor > 0:
                        glyph_idx += 2**exp
                glyph = glut[basis[0]][basis[1]][glyph_idx]
                y_strip.append( Segment( glyph, style ) )
            strips.append( Strip(y_strip) )
        return strips

    @staticmethod
    def _chunk_join( strips, chunk ):
        if len( strips ) == 0: return chunk
        joint = []
        for idx, line in enumerate( strips ):
            joint.append(Strip.join( (line,chunk[idx]) ))
        return joint

    @staticmethod
    def from_renderable( 
            phrase,
            basis = (2,4), 
            pips = False,
            font_size: int = 12,
            font_name: str = "TerminusTTF-4.46.0.ttf"
            ) -> List[List[Segment]]:
        strips = []
        con_strips = Console().render_lines( phrase )
        for a_strip in con_strips:
            for seg in a_strip:
                pane = ToGlyxels._font_pane( seg.text, font_name, font_size )
                chunk = ToGlyxels.pane2strips( seg.style, basis, pane, pips )
                strips = ToGlyxels._chunk_join( strips, chunk )
        return strips

    @staticmethod
    def from_string( 
            phrase: str,
            basis = (2,4), 
            pips = False,
            font_size: int = 12,
            font_name: str = "TerminusTTF-4.46.0.ttf"
            ) -> List[List[Segment]]:
        pane = ToGlyxels._font_pane( phrase, font_name, font_size )
        return ToGlyxels.pane2strips( None, basis, pane, pips )

    @staticmethod
    def _font_pane( phrase, font_name, font_size ):
        font_asset = resources.files().joinpath( "assets", font_name )
        font = ImageFont.truetype( font_asset, size=font_size )
        l,t,r,b = font.getbbox( phrase )
        mask = [x for x in font.getmask(phrase, mode='1')]
        return (r,b,mask)

