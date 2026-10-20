"""Map an Aside browser profile name to its native profile UUID and Aside account id."""
import json, pathlib

ROOT = pathlib.Path.home() / 'Library/Application Support/Aside'
ACCOUNTS = pathlib.Path.home() / '.aside/accounts.json'
IMPORT_PREFIX = 'Chrome · '


def label_of(name):
    """Imported profiles are shown as 'Chrome · <name>'; the tool uses the short name."""
    return name[len(IMPORT_PREFIX):] if name.startswith(IMPORT_PREFIX) else name


def list_profiles():
    state = json.loads((ROOT / 'Local State').read_text())
    labels = {}
    for folder, info in state['profile']['info_cache'].items():
        label = label_of(info.get('name') or '')
        if label:
            labels.setdefault(label, []).append(folder)
    return labels


def resolve_profile(profile):
    matches = list_profiles().get(profile, [])
    if len(matches) != 1:
        raise ValueError('Aside profile must exist uniquely: ' + profile)
    folder = ROOT / matches[0]
    prefs = json.loads((folder / 'Preferences').read_text())
    profile_id = prefs['aside']['profile_id']
    accounts = json.loads(ACCOUNTS.read_text())
    binding = accounts['profileAccountBindings'].get(profile_id)
    if not binding or pathlib.Path(binding['profilePath']).resolve() != folder.resolve():
        raise ValueError('Aside account/profile binding mismatch')
    if binding.get('profileId') != profile_id or not isinstance(binding.get('accountId'), int):
        raise ValueError('Invalid Aside account binding')
    return {'name': profile, 'path': str(folder), 'profile_id': profile_id,
            'account': 'u' + str(binding['accountId'])}
