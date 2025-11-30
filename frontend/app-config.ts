// frontend/app-config.ts

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
  companyName: 'Zepto',
  pageTitle: 'Zepto — Voice Commerce Agent',
  pageDescription:
    'Browse products, compare options, and place orders using only your voice. ACP-inspired shopping agent built with LiveKit and Murf Falcon.',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/Zepto-logo.svg', // optional, or keep existing if you had one
  accent: '#22c55e',
  logoDark: '/Zepto-logo-dark.svg',
  accentDark: '#22c55e',
  startButtonText: 'Start shopping',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
