import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.lokworld.channel',
  appName: '洛克世界频道',
  webDir: 'dist',
  server: {
    // 开发环境配置
    androidScheme: 'https',
  },
  android: {
    // Android 构建配置
    backgroundColor: '#ffffff',
    allowMixedContent: true,
    captureInput: true,
    webContentsDebuggingEnabled: false,
    // 包名
    packageId: 'com.lokworld.channel',
    // 版本配置
    versionCode: 1,
    // 插件配置
    plugins: {
      SplashScreen: {
        launchShowDuration: 2000,
        launchAutoHide: true,
        backgroundColor: '#ffffff',
        androidSplashResourceName: 'splash',
        androidScaleType: 'CENTER_CROP',
        showSpinner: false,
        splashFullScreen: true,
        splashImmersive: true,
      },
      StatusBar: {
        style: 'LIGHT',
        backgroundColor: '#4CAF50',
      },
    },
  },
  plugins: {
    // 悬浮窗插件配置
    FloatingWindow: {
      enabled: true,
      defaultPosition: 'bottom-right',
    },
    // 权限插件
    Permissions: {
      camera: {
        prompt: '需要相机权限来拍照上传头像',
      },
      geolocation: {
        prompt: '需要位置权限来推荐附近玩家',
      },
    },
  },
};

export default config;
