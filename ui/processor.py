import os
import tempfile
from xml.etree.ElementTree import Element, XML, parse

from fontTools.ttLib import TTFont


class FontProcessor(object):
    EXTENSIONS = ['ttf', 'woff', 'woff2']
    USE_TMP = False

    def __init__(self, ttf, mapping):
        self.ttf = ttf
        self.mapping = mapping

        self.xml_file = None
        self.xml_out_file = None

        self.charmap = {}
        self.chars_to_add = []
        self.glyph_by_name = {}

        self.prepare()
        self.process()

    def prepare(self):
        self.charmap = {}
        self.chars_to_add = self.get_chars()

        tmp1 = tempfile.mktemp(suffix='.xml')

        if self.USE_TMP:
            tmp2 = tempfile.mktemp(suffix='.xml')
        else:
            tmp2 = 'temp/tmp.xml'

        self.xml_file = tmp1
        self.xml_out_file = tmp2

        self.ttf.saveXML(self.xml_file)

        print(self.chars_to_add)

    def create_preview(self, output_dir, font_name):
        icon_template = '''<tr><td class="testarea">{ligature}</td><td>{ligature}</td><td>{name}</td></tr>'''

        icons = []
        for lig in self.mapping:
            icons.append(icon_template.format(
                ligature=lig,
                name=self.mapping[lig],
            ))

        template = '''
            <html>
                <head>
                    <style type="text/css">
                        @font-face {{
                            font-family: "{font_name}";
                            src: url("{font_name}.ttf") format("truetype");
                        }}

                        .testarea {{
                            font-family: "{font_name}" !important;
                            font-size: 30px;
                            display: block;
                        }}

                        .x {{
                            content: "\e001";
                        }}
                    </style>
                </head>
                <body>
                    <table>
                        <tr>
                            <th>Icon</th>
                            <th>Ligature</th>
                            <th>Name</th>
                        </tr>
                        {icons}
                    </table>
                </body>
            </html>
        '''.format(font_name=font_name, icons=''.join(icons))

        out_filename = '{}/{}_preview.html'.format(output_dir, font_name)
        with open(out_filename, 'w') as file:
            file.write(template)

    def process(self):

        xml_file = parse(self.xml_file)
        root = xml_file.getroot()

        self.parse_maps(root)
        self.parse_glyfs(root)
        self.add_gdef(root)
        self.add_order(root)
        self.add_to_hmtx(root)
        self.add_gpos(root)
        self.add_ligatures(root)

        xml_file.write(self.xml_out_file)

    def save_files(self, output_dir, font_name):
        ttf = TTFont()
        ttf.importXML(self.xml_out_file)

        for extension in self.EXTENSIONS:
            out_filename = '{}/{}.{}'.format(output_dir, font_name, extension)
            ttf.save(out_filename)

        self.create_preview(output_dir, font_name)

        self.cleanup()

    def cleanup(self):
        if self.xml_file:
            os.unlink(self.xml_file)
        if self.xml_out_file and not self.USE_TMP:
            os.unlink(self.xml_out_file)

    def get_chars(self):
        chars = set()

        for key in self.mapping.keys():
            chars = chars.union(list(key))

        return list(chars)

    def add_gdef(self, element):
        gdef = element.find('GDEF/GlyphClassDef')
        coverage = element.find('GDEF/LigCaretList/Coverage')
        coverage.attrib['Format'] = '1'

        # upgrade class
        for cls in gdef.findall('ClassDef'):
            cls.attrib['class'] = '2'

        for char in self.chars_to_add:
            new_def = Element('ClassDef', attrib={
                'glyph': char,
                'class': '1',
            })
            gdef.append(new_def)

    def add_gpos(self, element):
        gpos = element.find('GPOS')

        if gpos:
            gpos.clear()
        else:
            gpos = Element('GPOS')
            element.append(gpos)

        version = XML('''
            <Version value="0x00010000"/>
        ''')

        script_list = XML('''
            <ScriptList>
              <ScriptRecord index="0">
                <ScriptTag value="latn"/>
                <Script>
                  <DefaultLangSys>
                    <ReqFeatureIndex value="65535"/>
                    <FeatureIndex index="0" value="0"/>
                  </DefaultLangSys>
                </Script>
              </ScriptRecord>
            </ScriptList>
        ''')

        feature_list = XML('''
            <FeatureList>
              <FeatureRecord index="0">
                <FeatureTag value="size"/>
                <Feature>
                  <FeatureParamsSize>
                    <DesignSize value="16.0"/>
                    <SubfamilyID value="0"/>
                    <SubfamilyNameID value="1"/>
                    <RangeStart value="0.0"/>
                    <RangeEnd value="0.0"/>
                  </FeatureParamsSize>
                </Feature>
              </FeatureRecord>
            </FeatureList>
        ''')

        lookup_list = XML('''
            <LookupList>
            </LookupList>
        ''')

        gpos.append(version)
        gpos.append(script_list)
        gpos.append(feature_list)
        gpos.append(lookup_list)

    def add_to_hmtx(self, element):
        hmtx = element.find('hmtx')

        for char in self.chars_to_add:
            el = Element('mtx', attrib={
                'name': char,
                'width': '0',
                'lsb': '0',
            })
            hmtx.append(el)

    def add_ligatures(self, element):
        sub = self.get_or_create_gsub(element)
        ligature_root = sub.find('LookupList/Lookup/LigatureSubst')

        liga_keys = list(self.mapping.keys())
        used_chars = []

        current_record = None
        for key in sorted(liga_keys, reverse=True):
            start_char = key[0]

            if start_char not in used_chars:
                current_record = self.create_liga_record(start_char, ligature_root)
                used_chars.append(start_char)

            self.add_ligature(current_record, key)

    def add_ligature(self, record, key):
        component_str = ','.join(key[1:])
        name = self.mapping[key]

        el = Element('Ligature', attrib={
            'components': component_str,
            'glyph': name,
        })
        record.append(el)

    @staticmethod
    def create_liga_record(char, ligature_root):
        el = Element('LigatureSet', attrib={
            'glyph': char
        })
        ligature_root.append(el)
        return el

    @staticmethod
    def get_or_create_gsub(element):
        sub = element.find('GSUB')

        if not sub:
            sub = Element('GSUB')
            element.append(sub)
        else:
            sub.clear()

        version = Element('Version', attrib={
            'value': '0x00010000',
        })
        script_list = XML('''
            <ScriptList>
              <!-- ScriptCount=1 -->
              <ScriptRecord index="0">
                <ScriptTag value="latn"/>
                <Script>
                  <DefaultLangSys>
                    <ReqFeatureIndex value="65535"/>
                    <!-- FeatureCount=1 -->
                    <FeatureIndex index="0" value="0"/>
                  </DefaultLangSys>
                  <!-- LangSysCount=0 -->
                </Script>
              </ScriptRecord>
            </ScriptList>
        ''')

        feature_list = XML('''
            <FeatureList>
              <!-- FeatureCount=1 -->
              <FeatureRecord index="0">
                <FeatureTag value="liga"/>
                <Feature>
                  <!-- LookupCount=1 -->
                  <LookupListIndex index="0" value="0"/>
                </Feature>
              </FeatureRecord>
            </FeatureList>
        ''')

        liga_set = XML('''
            <LookupList>
                <Lookup index="0">
                    <LookupType value="4"></LookupType>
                    <LookupFlag value="0"></LookupFlag>
                    <LigatureSubst index="0" Format="1"></LigatureSubst>
                </Lookup>
            </LookupList>
        ''')

        sub.append(version)
        sub.append(script_list)
        sub.append(feature_list)
        sub.append(liga_set)
        return sub

    def parse_maps(self, element):
        for char_map in element.find('cmap'):
            if 'cmap_format_' in char_map.tag:
                self.parse_map(char_map)

    def parse_map(self, char_map):
        for char in self.chars_to_add:
            char_code = '{}'.format(hex(ord(char)))

            for mapping in char_map.findall('map'):
                mapping_code = '{}'.format(mapping.attrib['code'])

                if mapping_code == char_code:
                    if mapping_code not in self.charmap:
                        self.charmap[mapping_code] = self.get_new_char_code()

                    if char_map.tag == 'cmap_format_0':
                        char_map.remove(mapping)
                    else:
                        mapping.attrib['code'] = self.charmap[mapping_code]

            char_element = Element('map', attrib={
                'code': char_code,
                'name': char,
            })
            char_map.append(char_element)

        for mapping in char_map.findall('map'):
            code = mapping.attrib['code']
            name = mapping.attrib['name']
            self.glyph_by_name[name] = code

    def get_new_char_code(self):
        code = len(self.charmap) + 1
        return "0xe%03d" % (code,)

    def add_order(self, element):
        order_element = element.find('GlyphOrder')

        old_elements = []
        for el in order_element.findall('GlyphID'):
            old_elements.append(el)

        new_id = len(old_elements)
        for char in reversed(self.chars_to_add):
            new_el = Element('GlyphID', attrib={
                'id': '{}'.format(new_id),
                'name': char,
            })
            new_id += 1
            order_element.append(new_el)

    def parse_glyfs(self, element):
        ok = self.parse_glyf(element)
        ok = ok or self.parse_ccf(element)

    def parse_glyf(self, element):
        glyf_element = element.find('glyf')

        if not glyf_element:
            return False

        for char in self.chars_to_add:
            snippet = '''
                <TTGlyph name="{}" xMin="0" yMin="0" xMax="0" yMax="0">
                      <contour>
                            <pt x="0" y="0" on="1"/>
                      </contour>
                      <instructions/>
                </TTGlyph>
            '''.format(char)

            new_element = XML(snippet)
            glyf_element.append(new_element)
        return True

    def parse_ccf(self, element):
        glyf_element = element.find('CFF/CFFFont/CharStrings')
        if not glyf_element:
            print('no cff')
            return False

        for char in self.chars_to_add:
            snippet = '''
                <CharString name="{}">
                  endchar
                </CharString>
            '''.format(char)

            new_element = XML(snippet)
            glyf_element.append(new_element)
        return True