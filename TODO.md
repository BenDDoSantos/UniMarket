# TODO List for User Persistence Implementation

## Data Manager Updates
- [ ] Add current_user_file path in __init__
- [ ] Load current_user from file in __init__ if exists
- [ ] Implement load_current_user() method
- [ ] Implement save_current_user(usuario_dict) method
- [ ] Ensure register_user saves nombre_completo as 'name'

## Login Screen Updates
- [ ] In do_login, after setting current_user, call save_current_user

## Perfil Screen Updates
- [ ] Ensure on_enter calls update_user_info
- [ ] Update update_user_info to use correct field names ('name' instead of 'nombre')

## Editar Perfil Screen Updates
- [ ] Ensure on_pre_enter loads from load_current_user
- [ ] Ensure save_profile updates the user correctly
