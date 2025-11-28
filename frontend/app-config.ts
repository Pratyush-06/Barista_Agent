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
  pageTitle: 'Zepto — Smart Order Voice Assistant',
  pageDescription: 'Fast 10-minute delivery with voice-activated order management powered by AI',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/zepto-logo.svg',
  accent: '#00A699',
  logoDark: '/zepto-logo-dark.svg',
  accentDark: '#00D9C4',
  startButtonText: 'Place Order',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
