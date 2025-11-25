export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Physics Wallah',
  pageTitle: 'Physics Wallah — Voice Tutor',
  pageDescription: 'Practice aloud with an interactive voice tutor inspired by Physics Wallah',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/pw-logo.svg',
  accent: '#00C853',
  logoDark: '/pw-logo-dark.svg',
  accentDark: '#00E676',
  startButtonText: 'Start Voice Tutor',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
