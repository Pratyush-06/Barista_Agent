export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Solo Leveling Dungeon',
  pageTitle: 'Solo Leveling — Dungeon Run Voice Game',
  pageDescription:
    'Enter the Gate as a low-rank Hunter. A Solo Leveling–inspired voice Game Master narrates your fate, tracks HP & inventory, and rolls the dice on every action.',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  // you can keep these logos if you don’t have your own yet
  logo: '/zepto-logo.svg',
  logoDark: '/zepto-logo-dark.svg',

  // dungeon-ish cyan accent
  accent: '#22D3EE',
  accentDark: '#06B6D4',

  // this text will appear on the main button
  startButtonText: 'Enter the Gate',

  // LiveKit Cloud sandbox config (leave as-is unless you set these)
  sandboxId: undefined,
  agentName: undefined,
};
