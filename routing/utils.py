def parse_maneuver(maneuver: dict) -> str:
    if not maneuver:
        return 'Lanjutkan perjalanan'
    
    type = maneuver.get('type')
    modifier = maneuver.get('modifier')
    exit = maneuver.get('exit')
    road_name = maneuver.get('name', '')
    
    def exit_indonesian(exit_num):
        try:
            exit_num = int(exit_num)
            if exit_num == 1:
                return 'pertama'
            elif exit_num == 2:
                return 'kedua'
            elif exit_num == 3:
                return 'ketiga'
            elif exit_num == 4:
                return 'keempat'
            else:
                return f'ke-{exit_num}'
        except:
            return ''
    
    instructions = {
        'depart': 'Mulai perjalanan dari lokasi ini',
        'arrive': 'Anda telah tiba di tujuan',
        'turn': {
            'left': 'Belok ke kiri',
            'right': 'Belok ke kanan',
            'sharp left': 'Belok tajam ke kiri',
            'sharp right': 'Belok tajam ke kanan',
            'slight left': 'Belok pelan ke kiri',
            'slight right': 'Belok pelan ke kanan',
            None: 'Belok'
        },
        'new name': f'Teruskan lurus menuju {road_name}',
        'roundabout': f'Masuk bundaran dan ambil keluar {exit_indonesian(exit)}',
        'rotary': f'Masuk lingkaran lalu keluar di keluar {exit_indonesian(exit)}',
        'fork': f'Ambil percabangan {_translate_modifier(modifier)}',
        'merge': f'Bergabung ke jalur {_translate_modifier(modifier)}',
        'on ramp': f'Masuk jalan tol {_translate_modifier(modifier)}',
        'off ramp': f'Keluar melalui jalan tol {_translate_modifier(modifier)}'
    }
    default_instruction = 'Teruskan mengikuti jalan'
    if type in instructions:
        if type == 'turn':
            return instructions['turn'].get(modifier, instructions['turn'][None])
        return instructions[type]
    
    return default_instruction

def _translate_modifier(modifier: str) -> str:
    modifiers = {
        'left': 'sebelah kiri',
        'right': 'sebelah kanan',
        'straight': 'lurus',
        'slight left': 'sedikit ke kiri',
        'slight right': 'sedikit ke kanan',
        None: ''
    }
    return modifiers.get(modifier, '')