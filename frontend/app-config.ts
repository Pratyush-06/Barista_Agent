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
  companyName: 'Slice Bank',
  pageTitle: 'Slice Bank — Voice Fraud Detection',
  pageDescription: 'AI-powered voice fraud detection and transaction verification for secure banking',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/slice-logo.svg',
  accent: '#FBBF24',
  logoDark: '/slice-logo-dark.svg',
  accentDark: '#F59E0B',
  startButtonText: 'Verify Transaction',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
