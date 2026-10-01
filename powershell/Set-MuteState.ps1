<#PSScriptInfo

.VERSION 1.0.1

.GUID 4d1438ae-0691-4fa4-8fdf-3ef8e73db79f

.AUTHOR PrateekSingh

.COMPANYNAME

.COPYRIGHT

.TAGS Powershell Audio API

.LICENSEURI

.PROJECTURI https://geekeefy.wordpress.com/2017/03/31/powershell-auto-mute-when-headphones-are-accidently-unplugged/

.ICONURI

.EXTERNALMODULEDEPENDENCIES

.REQUIREDSCRIPTS

.EXTERNALSCRIPTDEPENDENCIES

.RELEASENOTES


#>

<#
.DESCRIPTION
Powershell script to automatically change the mute state of your sound physically plugged-in
headphones are plugged in or unplugged.

To launch this script automatically when your system starts you can add it to your scheduled tasks.
1. Open Task Scheduler and create a new task.
2. Give the task a name and a description.

General
1. Under security warnings, check the box to run whether the user is logged in or not.
2. Check the "Hidden" box.

Trigger
1. Set the trigger to "At log in".
2. Set the action to "Start a program" and browse to the location of this script.
3. Configure any additional settings as needed and save the task.

Actions
1. Set the action to "Start a program".
2. Set the Program/script to "powershell".
3. Set the Add arguments to the following. This bypasses the prompt PowerShell typically shows
    when running scripts when the execution policy is not set to bypass.
      "-ExecutionPolicy Bypass .\Set-MuteState.ps1".
4.Configure the Start in field to the directory where this script is located.

Make any other changes to the task, as desired, and save it. Reboot for the task to take effect
automatically. Optionally, you can manually trigger the task from the Task Scheduler to verify
that it works as expected.
#>

[CmdletBinding()]
Param()

#Adding definitions for accessing the Audio API
Add-Type -TypeDefinition @'
using System.Runtime.InteropServices;
[Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioEndpointVolume {
  // f(), g(), ... are unused COM method slots. Define these if you care
  int f(); int g(); int h(); int i();
  int SetMasterVolumeLevelScalar(float fLevel, System.Guid pguidEventContext);
  int j();
  int GetMasterVolumeLevelScalar(out float pfLevel);
  int k(); int l(); int m(); int n();
  int SetMute([MarshalAs(UnmanagedType.Bool)] bool bMute, System.Guid pguidEventContext);
  int GetMute(out bool pbMute);
}
[Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice {
  int Activate(ref System.Guid id, int clsCtx, int activationParams, out IAudioEndpointVolume aev);
}
[Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator {
  int f(); // Unused
  int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice endpoint);
}
[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")] class MMDeviceEnumeratorComObject { }
public class Audio {
  static IAudioEndpointVolume Vol() {
    var enumerator = new MMDeviceEnumeratorComObject() as IMMDeviceEnumerator;
    IMMDevice dev = null;
    Marshal.ThrowExceptionForHR(enumerator.GetDefaultAudioEndpoint(/*eRender*/ 0, /*eMultimedia*/ 1, out dev));
    IAudioEndpointVolume epv = null;
    var epvid = typeof(IAudioEndpointVolume).GUID;
    Marshal.ThrowExceptionForHR(dev.Activate(ref epvid, /*CLSCTX_ALL*/ 23, 0, out epv));
    return epv;
  }
  public static float Volume {
    get {float v = -1; Marshal.ThrowExceptionForHR(Vol().GetMasterVolumeLevelScalar(out v)); return v;}
    set {Marshal.ThrowExceptionForHR(Vol().SetMasterVolumeLevelScalar(value, System.Guid.Empty));}
  }
  public static bool Mute {
    get { bool mute; Marshal.ThrowExceptionForHR(Vol().GetMute(out mute)); return mute; }
    set { Marshal.ThrowExceptionForHR(Vol().SetMute(value, System.Guid.Empty)); }
  }
}
'@ -Verbose


While ($true) {
  # clean all events in the current session since its in a infinite loop,
  # to make a fresh start when loop begins
  Get-Event | Remove-Event -ErrorAction SilentlyContinue

  # registering the event and waiting for event to be triggered
  Register-WmiEvent -Class Win32_DeviceChangeEvent
  Wait-Event -OutVariable Event | Out-Null

  $EventType = $Event.sourceargs.newevent | `
    Sort-Object TIME_CREATED -Descending | `
    Select-Object EventType -ExpandProperty EventType -First 1

  # conditional logic to handle when to mute/unmute the machine using the Audio API
  if ($EventType -eq 3) {
    [Audio]::Mute = $true
    Write-Verbose "Muted [$((Get-Date).tostring())]"
  }
  elseif ($EventType -eq 2 -and [Audio]::Mute -eq $true) {
    [Audio]::Mute = $false
    Write-Verbose "UnMuted [$((Get-Date).tostring())]"
  }
}
