# TODO: Redesign Login and Register Screens

## Steps to Complete

- [ ] Update login_screen.py build_ui method:
  - Restructure to root MDBoxLayout vertical.
  - Add logo (size dp(120)).
  - Add MDCard with elevation=1, padding=dp(20), spacing=dp(18), size_hint=(0.90, None), height=dp(420), pos_hint={"center_x": 0.5, "center_y": 0.55}, radius=[20,20,20,20].
  - Inside card: Title "UniMarket" font_style="H4", subtitle "Marketplace Universitario" theme_text_color="Secondary".
  - Add email and password fields.
  - Add error label.
  - Add login button (MDRaisedButton with md_bg_color=(0/255, 94/255, 184/255, 1)).
  - Add register button (MDFlatButton with text_color=(0/255, 94/255, 184/255, 1)).
  - Keep all other methods unchanged.

- [ ] Update register_screen.py build_ui method:
  - Restructure to root MDBoxLayout vertical.
  - Add logo (size dp(120)).
  - After logo, add MDLabel(size_hint_y=0.06).
  - Add MDCard with same properties as login.
  - Inside card: Spacer MDLabel(size_hint_y=None, height=dp(10)) before title.
  - Title "Registro" font_style="H4".
  - Subtitle "Crea tu cuenta en UniMarket" theme_text_color="Secondary", height=dp(22).
  - Add email, password, confirm_password fields.
  - Add error label.
  - Add register button (MDRaisedButton with md_bg_color=(0/255, 94/255, 184/255, 1)).
  - Add back button (MDFlatButton with text_color=(0/255, 94/255, 184/255, 1)).
  - Keep all other methods unchanged.

- [ ] Test the UI changes:
  - Run the app.
  - Check centering, colors, spacing.
  - Verify functionality: login, register, navigation, validations.
  - Ensure no logic changes.
