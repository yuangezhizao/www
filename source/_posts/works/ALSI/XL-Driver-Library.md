---
title: Python 获取 CANoe 设备序列号
date: 2021-1-13 19:54:45
tags:
  - Vector
count: 1
os: 0
os_1: 10.0.17763.1637 2019-LTSC
browser: 0
browser_1: 86.0.4240.198 Stable
place: 新家
key: 107
---
    跑路（确信
<!-- more -->
## 0x00.前言
业务场景需要，详见：https://github.com/yuangezhizao/device_manager

## 0x01.[XL-Driver-Library](https://www.vector.com/int/en/products/products-a-z/libraries-drivers/xl-driver-library/)
> The XL-Driver-Library is a universal programming interface you can use to create your own applications while accessing Vector’s powerful hardware interfaces.
You can get the latest version of the library free-of-charge in our downloads. It contains vxlapi.dll and the .NET wrapper for .NET 3.5 or higher applications.

[下载](http://download.vectordownloads.cn/drivers/XL-Driver-Library_V11.6.12.zip)得到`XL-Driver-Library_V11.6.12.zip`，解压安装后路径为`C:\Users\Public\Documents\Vector\XL Driver Library 11.6.12`
![XL Driver Library 11.6.12](https://i1.yuangezhizao.cn/Win-10/20210113200052.jpg!webp)

`bin`目录里面的`dll`是通用库，其实读到最后就会知道只需要这个`dll`就足够了
![bin](https://i1.yuangezhizao.cn/Win-10/20210113200209.jpg!webp)

`doc`目录里是一个`PDF`手册，`exec`目录里则是预编译好的可执行二进制文件，示例工程都在`samples`目录下，举个栗子，打开这个`C++`工程（纯`C`的工程就不看了
![xlCANdemo_Csharp](https://i1.yuangezhizao.cn/Win-10/20210113201458.jpg!webp)

<details><summary>点击此处 ← 查看代码</summary>

``` C++
/*-------------------------------------------------------------------------------------------
| File        : Class1.cs
| Project     : Vector CAN .NET Example
|
| Description : This example demonstrates the basic CAN functionality of the XL.NET Driver Library
|--------------------------------------------------------------------------------------------
| Copyright (c) 2020 by Vector Informatik GmbH.  All rights reserved.
|-------------------------------------------------------------------------------------------*/

using System;
using System.Threading;
using Microsoft.Win32.SafeHandles;
using vxlapi_NET;


namespace xlCANDemo {
  /// <summary>
  /// Summary description for Class1.
  /// </summary>
  class Class1 {
    // -----------------------------------------------------------------------------------------------
    // Global variables
    // -----------------------------------------------------------------------------------------------
    // Driver access through XLDriver (wrapper)
    private static XLDriver CANDemo = new XLDriver();
    private static String appName = "xlCANdemoNET";

    // Driver configuration
    private static XLClass.xl_driver_config driverConfig = new XLClass.xl_driver_config();

    // Variables required by XLDriver
    private static XLDefine.XL_HardwareType hwType = XLDefine.XL_HardwareType.XL_HWTYPE_NONE;
    private static uint hwIndex = 0;
    private static uint hwChannel = 0;
    private static int portHandle = -1;
    private static UInt64 accessMask = 0;
    private static UInt64 permissionMask = 0;
    private static UInt64 txMask = 0;
    private static UInt64 rxMask = 0;
    private static int txCi = -1;
    private static int rxCi = -1;
    private static EventWaitHandle xlEvWaitHandle = new EventWaitHandle(false, EventResetMode.AutoReset, null);

    // RX thread
    private static Thread rxThread;
    private static bool blockRxThread = false;
    // -----------------------------------------------------------------------------------------------




    // -----------------------------------------------------------------------------------------------
    /// <summary>
    /// MAIN
    /// 
    /// Sends and receives CAN messages using main methods of the "XLDriver" class.
    /// This demo requires two connected CAN channels (Vector network interface). 
    /// The configuration is read from Vector Hardware Config (vcanconf.exe).
    /// </summary>
    // -----------------------------------------------------------------------------------------------
    [STAThread]
    static int Main(string[] args) {
      XLDefine.XL_Status status;

      Console.WriteLine("-------------------------------------------------------------------");
      Console.WriteLine("                     xlCANdemo.NET C# V11.6                        ");
      Console.WriteLine("Copyright (c) 2020 by Vector Informatik GmbH.  All rights reserved.");
      Console.WriteLine("-------------------------------------------------------------------\n");

      // print .NET wrapper version
      Console.WriteLine("vxlapi_NET        : " + typeof(XLDriver).Assembly.GetName().Version);

      // Open XL Driver
      status = CANDemo.XL_OpenDriver();
      Console.WriteLine("Open Driver       : " + status);
      if (status != XLDefine.XL_Status.XL_SUCCESS) PrintFunctionError();


      // Get XL Driver configuration
      status = CANDemo.XL_GetDriverConfig(ref driverConfig);
      Console.WriteLine("Get Driver Config : " + status);
      if (status != XLDefine.XL_Status.XL_SUCCESS) PrintFunctionError();


      // Convert the dll version number into a readable string
      Console.WriteLine("DLL Version       : " + CANDemo.VersionToString(driverConfig.dllVersion));


      // Display channel count
      Console.WriteLine("Channels found    : " + driverConfig.channelCount);


      // Display all found channels
      for (int i = 0; i < driverConfig.channelCount; i++) {
        Console.WriteLine("\n                   [{0}] " + driverConfig.channel[i].name, i);
        Console.WriteLine("                    - Channel Mask    : " + driverConfig.channel[i].channelMask);
        Console.WriteLine("                    - Transceiver Name: " + driverConfig.channel[i].transceiverName);
        Console.WriteLine("                    - Serial Number   : " + driverConfig.channel[i].serialNumber);
      }

      // If the application name cannot be found in VCANCONF...
      if ((CANDemo.XL_GetApplConfig(appName, 0, ref hwType, ref hwIndex, ref hwChannel, XLDefine.XL_BusTypes.XL_BUS_TYPE_CAN) != XLDefine.XL_Status.XL_SUCCESS) ||
          (CANDemo.XL_GetApplConfig(appName, 1, ref hwType, ref hwIndex, ref hwChannel, XLDefine.XL_BusTypes.XL_BUS_TYPE_CAN) != XLDefine.XL_Status.XL_SUCCESS)) {
        //...create the item with two CAN channels
        CANDemo.XL_SetApplConfig(appName, 0, XLDefine.XL_HardwareType.XL_HWTYPE_NONE, 0, 0, XLDefine.XL_BusTypes.XL_BUS_TYPE_CAN);
        CANDemo.XL_SetApplConfig(appName, 1, XLDefine.XL_HardwareType.XL_HWTYPE_NONE, 0, 0, XLDefine.XL_BusTypes.XL_BUS_TYPE_CAN);
        PrintAssignErrorAndPopupHwConf();
      }

      // Request the user to assign channels until both CAN1 (Tx) and CAN2 (Rx) are assigned to usable channels
      while (!GetAppChannelAndTestIsOk(0, ref txMask, ref txCi) || !GetAppChannelAndTestIsOk(1, ref rxMask, ref rxCi))
      {
        PrintAssignErrorAndPopupHwConf();
      }

      PrintConfig();

      accessMask = txMask | rxMask;
      permissionMask = accessMask;

      // Open port
      status = CANDemo.XL_OpenPort(ref portHandle, appName, accessMask, ref permissionMask, 1024, XLDefine.XL_InterfaceVersion.XL_INTERFACE_VERSION, XLDefine.XL_BusTypes.XL_BUS_TYPE_CAN);
      Console.WriteLine("\n\nOpen Port             : " + status);
      if (status != XLDefine.XL_Status.XL_SUCCESS) PrintFunctionError();

      // Check port
      status = CANDemo.XL_CanRequestChipState(portHandle, accessMask);
      Console.WriteLine("Can Request Chip State: " + status);
      if (status != XLDefine.XL_Status.XL_SUCCESS) PrintFunctionError();

      // Activate channel
      status = CANDemo.XL_ActivateChannel(portHandle, accessMask, XLDefine.XL_BusTypes.XL_BUS_TYPE_CAN, XLDefine.XL_AC_Flags.XL_ACTIVATE_NONE);
      Console.WriteLine("Activate Channel      : " + status);
      if (status != XLDefine.XL_Status.XL_SUCCESS) PrintFunctionError();

      // Initialize EventWaitHandle object with RX event handle provided by DLL
      int tempInt = -1;
      status = CANDemo.XL_SetNotification(portHandle, ref tempInt, 1);
      xlEvWaitHandle.SafeWaitHandle = new SafeWaitHandle(new IntPtr(tempInt), true);

      Console.WriteLine("Set Notification      : " + status);
      if (status != XLDefine.XL_Status.XL_SUCCESS) PrintFunctionError();

      // Reset time stamp clock
      status = CANDemo.XL_ResetClock(portHandle);
      Console.WriteLine("Reset Clock           : " + status + "\n\n");
      if (status != XLDefine.XL_Status.XL_SUCCESS) PrintFunctionError();

      // Run Rx Thread
      Console.WriteLine("Start Rx thread...");
      rxThread = new Thread(new ThreadStart(RXThread));
      rxThread.Start();

      // User information
      Console.WriteLine("Press <ENTER> to transmit CAN messages \n  <b>, <ENTER> to block Rx thread for rx-overrun-test \n  <B>, <ENTER> burst of CAN TX messages \n  <x>, <ENTER> to exit");

      // Transmit CAN data
      while (true) {
        if (blockRxThread) Console.WriteLine("Rx thread blocked.");


        // Read user input
        string str = Console.ReadLine();
        if (str == "b") blockRxThread = !blockRxThread;
        else if (str == "B") {
          for (int i = 0; i < 1000; i++) {
            // Burst of CAN frames
            CANTransmitDemo();
          }
        }
        else if (str == "x") break;
        else {
          // Send CAN frames
          CANTransmitDemo();
        }
      }

      // Kill Rx thread
      rxThread.Abort();
      Console.WriteLine("Close Port                     : " + CANDemo.XL_ClosePort(portHandle));
      Console.WriteLine("Close Driver                   : " + CANDemo.XL_CloseDriver());

      return 0;
    }
    // -----------------------------------------------------------------------------------------------




    // -----------------------------------------------------------------------------------------------
    /// <summary>
    /// Error message/exit in case of a functional call does not return XL_SUCCESS
    /// </summary>
    // -----------------------------------------------------------------------------------------------
    private static int PrintFunctionError() {
      Console.WriteLine("\nERROR: Function call failed!\nPress any key to continue...");
      Console.ReadKey();
      return -1;
    }
    // -----------------------------------------------------------------------------------------------




    // -----------------------------------------------------------------------------------------------
    /// <summary>
    /// Displays the Vector Hardware Configuration.
    /// </summary>
    // -----------------------------------------------------------------------------------------------
    private static void PrintConfig() {
      Console.WriteLine("\n\nAPPLICATION CONFIGURATION");

      foreach (int channelIndex in new int[] {txCi, rxCi}) {
        Console.WriteLine("-------------------------------------------------------------------");
        Console.WriteLine("Configured Hardware Channel : " + driverConfig.channel[channelIndex].name);
        Console.WriteLine("Hardware Driver Version     : " + CANDemo.VersionToString(driverConfig.channel[channelIndex].driverVersion));
        Console.WriteLine("Used Transceiver            : " + driverConfig.channel[channelIndex].transceiverName);
      }

      Console.WriteLine("-------------------------------------------------------------------\n");
    }
    // -----------------------------------------------------------------------------------------------




    // -----------------------------------------------------------------------------------------------
    /// <summary>
    /// Error message if channel assignment is not valid and popup VHwConfig, so the user can correct the assignment
    /// </summary>
    // -----------------------------------------------------------------------------------------------
    private static void PrintAssignErrorAndPopupHwConf() {
      Console.WriteLine("\nPlease check application settings of \"" + appName + " CAN1/CAN2\",\nassign them to available hardware channels and press enter.");
      CANDemo.XL_PopupHwConfig();
      Console.ReadKey();
    }
    // -----------------------------------------------------------------------------------------------

    // -----------------------------------------------------------------------------------------------
    /// <summary>
    /// Retrieve the application channel assignment and test if this channel can be opened
    /// </summary>
    // -----------------------------------------------------------------------------------------------
    private static bool GetAppChannelAndTestIsOk(uint appChIdx, ref UInt64 chMask, ref int chIdx)
    {
      XLDefine.XL_Status status = CANDemo.XL_GetApplConfig(appName, appChIdx, ref hwType, ref hwIndex, ref hwChannel, XLDefine.XL_BusTypes.XL_BUS_TYPE_CAN);
      if (status != XLDefine.XL_Status.XL_SUCCESS)
      {
        Console.WriteLine("XL_GetApplConfig      : " + status);
        PrintFunctionError();
      }

      chMask = CANDemo.XL_GetChannelMask(hwType, (int)hwIndex, (int)hwChannel);
      chIdx = CANDemo.XL_GetChannelIndex(hwType, (int)hwIndex, (int)hwChannel);
      if (chIdx < 0 || chIdx >= driverConfig.channelCount)
      {
        // the (hwType, hwIndex, hwChannel) triplet stored in the application configuration does not refer to any available channel.
        return false;
      }

      // test if CAN is available on this channel
      return (driverConfig.channel[chIdx].channelBusCapabilities & XLDefine.XL_BusCapabilities.XL_BUS_ACTIVE_CAP_CAN) != 0;
    }
    // -----------------------------------------------------------------------------------------------




    // -----------------------------------------------------------------------------------------------
    /// <summary>
    /// Sends some CAN messages.
    /// </summary>
    // ----------------------------------------------------------------------------------------------- 
    public static void CANTransmitDemo() {
      XLDefine.XL_Status txStatus;

      // Create an event collection with 2 messages (events)
      XLClass.xl_event_collection xlEventCollection = new XLClass.xl_event_collection(2);

      // event 1
      xlEventCollection.xlEvent[0].tagData.can_Msg.id = 0x100;
      xlEventCollection.xlEvent[0].tagData.can_Msg.dlc = 8;
      xlEventCollection.xlEvent[0].tagData.can_Msg.data[0] = 1;
      xlEventCollection.xlEvent[0].tagData.can_Msg.data[1] = 2;
      xlEventCollection.xlEvent[0].tagData.can_Msg.data[2] = 3;
      xlEventCollection.xlEvent[0].tagData.can_Msg.data[3] = 4;
      xlEventCollection.xlEvent[0].tagData.can_Msg.data[4] = 5;
      xlEventCollection.xlEvent[0].tagData.can_Msg.data[5] = 6;
      xlEventCollection.xlEvent[0].tagData.can_Msg.data[6] = 7;
      xlEventCollection.xlEvent[0].tagData.can_Msg.data[7] = 8;
      xlEventCollection.xlEvent[0].tag = XLDefine.XL_EventTags.XL_TRANSMIT_MSG;

      // event 2
      xlEventCollection.xlEvent[1].tagData.can_Msg.id = 0x200;
      xlEventCollection.xlEvent[1].tagData.can_Msg.dlc = 8;
      xlEventCollection.xlEvent[1].tagData.can_Msg.data[0] = 9;
      xlEventCollection.xlEvent[1].tagData.can_Msg.data[1] = 10;
      xlEventCollection.xlEvent[1].tagData.can_Msg.data[2] = 11;
      xlEventCollection.xlEvent[1].tagData.can_Msg.data[3] = 12;
      xlEventCollection.xlEvent[1].tagData.can_Msg.data[4] = 13;
      xlEventCollection.xlEvent[1].tagData.can_Msg.data[5] = 14;
      xlEventCollection.xlEvent[1].tagData.can_Msg.data[6] = 15;
      xlEventCollection.xlEvent[1].tagData.can_Msg.data[7] = 16;
      xlEventCollection.xlEvent[1].tag = XLDefine.XL_EventTags.XL_TRANSMIT_MSG;


      // Transmit events
      txStatus = CANDemo.XL_CanTransmit(portHandle, txMask, xlEventCollection);
      Console.WriteLine("Transmit Message      : " + txStatus);
    }
    // -----------------------------------------------------------------------------------------------




    // -----------------------------------------------------------------------------------------------
    /// <summary>
    /// EVENT THREAD (RX)
    /// 
    /// RX thread waits for Vector interface events and displays filtered CAN messages.
    /// </summary>
    // ----------------------------------------------------------------------------------------------- 
    public static void RXThread() {
      // Create new object containing received data 
      XLClass.xl_event receivedEvent = new XLClass.xl_event();

      // Result of XL Driver function calls
      XLDefine.XL_Status xlStatus = XLDefine.XL_Status.XL_SUCCESS;


      // Note: this thread will be destroyed by MAIN
      while (true) {
        // Wait for hardware events
        if (xlEvWaitHandle.WaitOne(1000)) {
          // ...init xlStatus first
          xlStatus = XLDefine.XL_Status.XL_SUCCESS;

          // afterwards: while hw queue is not empty...
          while (xlStatus != XLDefine.XL_Status.XL_ERR_QUEUE_IS_EMPTY) {
            // ...block RX thread to generate RX-Queue overflows
            while (blockRxThread) { Thread.Sleep(1000); }

            // ...receive data from hardware.
            xlStatus = CANDemo.XL_Receive(portHandle, ref receivedEvent);

            //  If receiving succeed....
            if (xlStatus == XLDefine.XL_Status.XL_SUCCESS) {
              if ((receivedEvent.flags & XLDefine.XL_MessageFlags.XL_EVENT_FLAG_OVERRUN) != 0) {
                Console.WriteLine("-- XL_EVENT_FLAG_OVERRUN --");
              }

              // ...and data is a Rx msg...
              if (receivedEvent.tag == XLDefine.XL_EventTags.XL_RECEIVE_MSG) {
                if ((receivedEvent.tagData.can_Msg.flags & XLDefine.XL_MessageFlags.XL_CAN_MSG_FLAG_OVERRUN) != 0) {
                  Console.WriteLine("-- XL_CAN_MSG_FLAG_OVERRUN --");
                }

                // ...check various flags
                if ((receivedEvent.tagData.can_Msg.flags & XLDefine.XL_MessageFlags.XL_CAN_MSG_FLAG_ERROR_FRAME)
                    == XLDefine.XL_MessageFlags.XL_CAN_MSG_FLAG_ERROR_FRAME) {
                  Console.WriteLine("ERROR FRAME");
                }

                else if ((receivedEvent.tagData.can_Msg.flags & XLDefine.XL_MessageFlags.XL_CAN_MSG_FLAG_REMOTE_FRAME)
                    == XLDefine.XL_MessageFlags.XL_CAN_MSG_FLAG_REMOTE_FRAME) {
                  Console.WriteLine("REMOTE FRAME");
                }

                else {
                  Console.WriteLine(CANDemo.XL_GetEventString(receivedEvent));
                }
              }
            }
          }
        }
        // No event occurred
      }
    }
    // -----------------------------------------------------------------------------------------------
  }
}
```

</details>

不想【查看代码】的话，就看下面这张截图，也足够能说明问题了
![serialNumber](https://i1.yuangezhizao.cn/Win-10/20210113201309.jpg!webp)

最后，再补一个`VB`版本的吧（

<details><summary>点击此处 ← 查看代码</summary>

``` VB
Option Explicit On

Imports System
Imports System.Runtime.InteropServices
Imports System.Threading
Imports vxlapi_NET


Namespace xlCANdemo

    ' <summary>
    ' Summary description for Class1.
    ' </summary>
    Class Class1

        ' -----------------------------------------------------------------------------------------------
        ' DLL Import for RX events
        ' -----------------------------------------------------------------------------------------------
        <DllImport("kernel32.dll", SetLastError:=True)> _
        Shared Function WaitForSingleObject(ByVal handle As Integer, ByVal timeOut As Integer) As Integer
        End Function
        ' -----------------------------------------------------------------------------------------------



        ' -----------------------------------------------------------------------------------------------
        ' Global variables
        ' -----------------------------------------------------------------------------------------------
        'create port channel object
        Shared appName As String = "xlCANdemoNET"
        Shared CANDemo As XLDriver = New XLDriver
        Shared driverConfig As XLClass.xl_driver_config = New XLClass.xl_driver_config
        Shared rxThread As Thread
        Shared input As String
        Shared hwType As UInt32
        Shared hwIndex As UInt32
        Shared hwChannel As UInt32
        Shared busTypeCAN As XLDefine.XL_BusTypes = XLDefine.XL_BusTypes.XL_BUS_TYPE_CAN
        Shared flags As UInt32
        Shared portHandle As Int32
        Shared eventHandle As Int32
        Shared accessMask As UInt64
        Shared txMask As UInt64
        Shared permissionMask As UInt64
        Shared channelIndex As Int32
        ' -----------------------------------------------------------------------------------------------



        ' -----------------------------------------------------------------------------------------------
        ' <summary>
        ' MAIN
        '
        ' Sends and receives CAN messages using main methods of the "XLDriver" class.
        ' This demo requires two connected CAN channels (Vector network interface).
        ' The configuration is read from Vector Hardware Config (vcanconf.exe).
        ' </summary>
        ' -----------------------------------------------------------------------------------------------
        <STAThread()> _
        Shared Sub Main()

            Dim i As Integer

            Console.WriteLine("-------------------------------------------------------------------")
            Console.WriteLine("                    xlCANdemo.NET VBnet V11.6                      ")
            Console.WriteLine("Copyright (c) 2020 by Vector Informatik GmbH.  All rights reserved.")
            Console.WriteLine("-------------------------------------------------------------------")

            ' Open XL Driver
            Console.WriteLine("Open Driver       : " + CANDemo.XL_OpenDriver().ToString())

            ' Get the complete XL Driver configuration, stored in driverConfig object
            Console.WriteLine("Get Driver Config : " + CANDemo.XL_GetDriverConfig(driverConfig).ToString())

            ' Convert the dll version to a readable string
            Console.WriteLine("DLL Version       : " + CANDemo.VersionToString(driverConfig.dllVersion))

            ' Display channel count
            Console.WriteLine("Channels found    : " + driverConfig.channelCount.ToString())

            ' Display found channels
            For i = 0 To (Convert.ToInt32(driverConfig.channelCount) - Convert.ToInt32(1))
                Console.WriteLine("                   [{0}] " + driverConfig.channel(i).name, i)
                Console.WriteLine("                    - Channel Mask    : " + driverConfig.channel(i).channelMask.ToString())
                Console.WriteLine("                    - Transceiver Name: " + driverConfig.channel(i).transceiverName.ToString())
                Console.WriteLine("                    - Serial Number   : " + driverConfig.channel(i).serialNumber.ToString())
                Console.WriteLine()
            Next

            ' If application not found in VCANCONF....
            If CANDemo.XL_GetApplConfig(appName, Convert.ToUInt32(0), hwType, hwIndex, hwChannel, busTypeCAN) <> XLDefine.XL_Status.XL_SUCCESS Or CANDemo.XL_GetApplConfig(appName, Convert.ToUInt32(1), hwType, hwIndex, hwChannel, busTypeCAN) <> XLDefine.XL_Status.XL_SUCCESS Then

                ' ..create the item with 2 channels
                CANDemo.XL_SetApplConfig(appName, Convert.ToUInt32(0), Convert.ToUInt32(0), Convert.ToUInt32(0), Convert.ToUInt32(0), Convert.ToUInt32(0))
                CANDemo.XL_SetApplConfig(appName, Convert.ToUInt32(1), Convert.ToUInt32(0), Convert.ToUInt32(0), Convert.ToUInt32(0), Convert.ToUInt32(0))
                PrintAssignError()

            Else
                Try

                    ' Read setting of CAN1
                    CANDemo.XL_GetApplConfig(appName, Convert.ToUInt32(0), hwType, hwIndex, hwChannel, busTypeCAN)
                    accessMask = CANDemo.XL_GetChannelMask(Convert.ToInt32(hwType), Convert.ToInt32(hwIndex), Convert.ToInt32(hwChannel))
                    txMask = accessMask
                    PrintConfig()

                    ' Read setting of CAN2
                    CANDemo.XL_GetApplConfig(appName, Convert.ToUInt32(1), hwType, hwIndex, hwChannel, busTypeCAN)
                    accessMask = Convert.ToUInt64(Convert.ToInt32(accessMask) Or Convert.ToInt32(CANDemo.XL_GetChannelMask(Convert.ToInt32(hwType), Convert.ToInt32(hwIndex), Convert.ToInt32(hwChannel))))

                    permissionMask = Convert.ToUInt64(Convert.ToInt32(accessMask) Or Convert.ToInt32(accessMask))
                    PrintConfig()

                    ' Open port
                    Console.WriteLine("Open Port             : " + CANDemo.XL_OpenPort(portHandle, appName, accessMask, permissionMask, Convert.ToUInt32(1024), XLDefine.XL_InterfaceVersion.XL_INTERFACE_VERSION, busTypeCAN).ToString())

                    ' Check port
                    Console.WriteLine("Can Request Chip State: " + CANDemo.XL_CanRequestChipState(portHandle, accessMask).ToString())

                    ' Activate channel
                    Console.WriteLine("Activate Channel      : " + CANDemo.XL_ActivateChannel(portHandle, accessMask, busTypeCAN, flags).ToString())

                    ' Get RX event handle
                    Console.WriteLine("Set Notification      : " + CANDemo.XL_SetNotification(portHandle, eventHandle, 1).ToString())

                    ' Reset time stamp clock
                    Console.WriteLine("Reset Clock           : " + CANDemo.XL_ResetClock(portHandle).ToString())

                    ' Create and start Rx thread
                    Dim rxThread As New Thread(AddressOf RX_Thread)
                    rxThread.Start()


                    Console.WriteLine("Press <ENTER> to transmit CAN data. Press <x>, <ENTER> to close application.")
                    While Not (Console.ReadLine Like "[xX]")
                        ' Transmit some data				
                        CANTransmitDemo()
                        Console.WriteLine("Transmitted")

                    End While

                    rxThread.Abort()


                Catch
                    ' No channel assigned to hardware
                    PrintAssignError()
                End Try
            End If
        End Sub
        ' -----------------------------------------------------------------------------------------------



        ' -----------------------------------------------------------------------------------------------
        ' <summary>
        ' Displays Vector Hardware Configuration.
        ' </summary>
        ' -----------------------------------------------------------------------------------------------
        Public Shared Sub PrintConfig()
            channelIndex = CANDemo.XL_GetChannelIndex(Convert.ToInt32(hwType), Convert.ToInt32(hwIndex), Convert.ToInt32(hwChannel))
            Console.WriteLine("APPLICATION CONFIGURATION")
            Console.WriteLine("-------------------------------------------------------------------")
            Console.WriteLine("Configured Hardware Channel : " + driverConfig.channel(channelIndex).name)
            Console.WriteLine("Hardware Driver Version     : " + CANDemo.VersionToString(driverConfig.channel(channelIndex).driverVersion))
            Console.WriteLine("Used Transceiver            : " + driverConfig.channel(channelIndex).transceiverName)
            Console.WriteLine("-------------------------------------------------------------------")
        End Sub
        ' -----------------------------------------------------------------------------------------------



        ' -----------------------------------------------------------------------------------------------
        ' <summary>
        ' Error message if channel assignment is not valid.
        ' </summary>
        ' -----------------------------------------------------------------------------------------------
        Public Shared Sub PrintAssignError()
            Console.WriteLine(Chr(10) + "Please check application settings of" + Chr(34) + appName + " CAN1/CAN2" + Chr(34) + Chr(10) + "and assign it to an available hardware channel and restart application.")
            CANDemo.XL_PopupHwConfig()
            Console.ReadLine()
        End Sub
        ' -----------------------------------------------------------------------------------------------



        ' -----------------------------------------------------------------------------------------------
        ' <summary>
        ' Sends some CAN messages.
        ' </summary>
        ' -----------------------------------------------------------------------------------------------
        Public Shared Sub CANTransmitDemo()

            Dim xlEventCollection As XLClass.xl_event_collection = New XLClass.xl_event_collection(Convert.ToUInt32(2))

            xlEventCollection.xlEvent(0).tagData.can_Msg.id = Convert.ToUInt32(&H100)
            xlEventCollection.xlEvent(0).tagData.can_Msg.dlc = Convert.ToUInt16(8)
            xlEventCollection.xlEvent(0).tagData.can_Msg.data(0) = Convert.ToByte(1)
            xlEventCollection.xlEvent(0).tagData.can_Msg.data(1) = Convert.ToByte(2)
            xlEventCollection.xlEvent(0).tagData.can_Msg.data(2) = Convert.ToByte(3)
            xlEventCollection.xlEvent(0).tagData.can_Msg.data(3) = Convert.ToByte(4)
            xlEventCollection.xlEvent(0).tagData.can_Msg.data(4) = Convert.ToByte(5)
            xlEventCollection.xlEvent(0).tagData.can_Msg.data(5) = Convert.ToByte(6)
            xlEventCollection.xlEvent(0).tagData.can_Msg.data(6) = Convert.ToByte(7)
            xlEventCollection.xlEvent(0).tagData.can_Msg.data(7) = Convert.ToByte(8)
            xlEventCollection.xlEvent(0).tag = XLDefine.XL_EventTags.XL_TRANSMIT_MSG

            xlEventCollection.xlEvent(1).tagData.can_Msg.id = Convert.ToUInt32(&H200)
            xlEventCollection.xlEvent(1).tagData.can_Msg.dlc = Convert.ToUInt16(8)
            xlEventCollection.xlEvent(1).tagData.can_Msg.data(0) = Convert.ToByte(9)
            xlEventCollection.xlEvent(1).tagData.can_Msg.data(1) = Convert.ToByte(10)
            xlEventCollection.xlEvent(1).tagData.can_Msg.data(2) = Convert.ToByte(11)
            xlEventCollection.xlEvent(1).tagData.can_Msg.data(3) = Convert.ToByte(12)
            xlEventCollection.xlEvent(1).tagData.can_Msg.data(4) = Convert.ToByte(13)
            xlEventCollection.xlEvent(1).tagData.can_Msg.data(5) = Convert.ToByte(14)
            xlEventCollection.xlEvent(1).tagData.can_Msg.data(6) = Convert.ToByte(15)
            xlEventCollection.xlEvent(1).tagData.can_Msg.data(7) = Convert.ToByte(16)
            xlEventCollection.xlEvent(1).tag = XLDefine.XL_EventTags.XL_TRANSMIT_MSG

            Console.WriteLine("Transmit Message      : " + CANDemo.XL_CanTransmit(portHandle, txMask, xlEventCollection).ToString())
        End Sub
        ' -----------------------------------------------------------------------------------------------



        ' -----------------------------------------------------------------------------------------------
        ' <summary>
        ' RXThread
        ' RX Thread waits for Vector interface events and displays filtered CAN messages.
        ' </summary>
        ' -----------------------------------------------------------------------------------------------
        Public Shared Sub RX_Thread()

            ' Create new object containing received data 
            Dim receivedEvent As XLClass.xl_event = New XLClass.xl_event

            ' Result of XL Driver function calls
            Dim xlStatus As XLDefine.XL_Status = XLDefine.XL_Status.XL_SUCCESS

            ' Result values of WaitForSingleObject 
            Dim waitResult As XLDefine.WaitResults = New XLDefine.WaitResults


            ' Note: this thread will be destroyed by MAIN
            While (True)

                ' Wait for hardware events
                waitResult = WaitForSingleObject(eventHandle, 1000)

                ' If event occured... 
                If (waitResult <> XLDefine.WaitResults.WAIT_TIMEOUT) Then

                    ' init xlStatus
                    xlStatus = XLDefine.XL_Status.XL_SUCCESS

                    ' afterwards: while hw queue not empty..,
                    While (xlStatus <> XLDefine.XL_Status.XL_ERR_QUEUE_IS_EMPTY)

                        ' ...receive data from hardware queue.
                        xlStatus = CANDemo.XL_Receive(portHandle, receivedEvent)

                        '  If receive succeed....
                        If (xlStatus = XLDefine.XL_Status.XL_SUCCESS) Then

                            ' ...and data was Rx msg...
                            If (receivedEvent.tag = XLDefine.XL_EventTags.XL_RECEIVE_MSG) Then

                                ' Check various flags
                                If ((receivedEvent.tagData.can_Msg.flags And XLDefine.XL_MessageFlags.XL_CAN_MSG_FLAG_ERROR_FRAME) = XLDefine.XL_MessageFlags.XL_CAN_MSG_FLAG_ERROR_FRAME) Then
                                    Console.WriteLine("ERROR FRAME")

                                ElseIf ((receivedEvent.tagData.can_Msg.flags And XLDefine.XL_MessageFlags.XL_CAN_MSG_FLAG_REMOTE_FRAME) = XLDefine.XL_MessageFlags.XL_CAN_MSG_FLAG_REMOTE_FRAME) Then
                                    Console.WriteLine("REMOTE FRAME")

                                    ' Print only "real" Rx messages
                                ElseIf ((receivedEvent.tagData.can_Msg.flags And XLDefine.XL_MessageFlags.XL_CAN_MSG_FLAG_TX_COMPLETED) = 0) Then
                                    Console.WriteLine(CANDemo.XL_GetEventString(receivedEvent))

                                End If

                            End If
                        End If
                    End While
                End If
                ' No event occured
            End While
            ' ------------------------------------------------------------------
        End Sub
    End Class
End Namespace
```

</details>

结果`VB`版本的看起来更简洁（哭笑不得……
![serialNumber](https://i1.yuangezhizao.cn/Win-10/20210113203448.jpg!webp)

当然还需要对照`PDF`手册看，不难得知`XLchannelConfig`这个结构体基本上包含了所有需要的东西
``` C
typedef struct s_xl_channel_config {
char           name [XL_MAX_LENGTH + 1];
unsigned cha   hwType;
unsigned char  hwIndex;
unsigned char  hwChannel;
unsigned short transceiverType;
unsigned int   transceiverState;
unsigned char  channelIndex;
XLuint64       channelMask;
unsigned int   channelCapabilities;
unsigned int   channelBusCapabilities;
unsigned char  isOnBus;
unsigned int   connectedBusType;
XLbusParams    busParams;
unsigned int   driverVersion;
unsigned int   interfaceVersion;
unsigned int   raw_data[10];
unsigned int   serialNumber;
unsigned int   articleNumber;
char           transceiverName [XL_MAX_LENGTH + 1];
unsigned int   specialCabFlags;
unsigned int   dominantTimeout;
unsigned in    reserved[8];
} XLchannelConfig;
```
不过成员`hwType`又需要参照`vxlapi.h`寻找具体的类型定义
![hwType](https://i1.yuangezhizao.cn/Win-10/20210113205236.jpg!webp)

只有搞懂了这个获取逻辑，才能用`py`的方式来写

## 0x02.[pythonnet - Python.NET](https://github.com/pythonnet/pythonnet)
没错，`Calling .NET code from Python！`
安装是`pip3 install pythonnet`可不是`pip3 install clr`（白天看到`import clr`就顺手进坑可太草了
常用的使用方式比如想加载`.NET`的程序集，就可以用`clr`的`AddReference`函数来实现
``` python
import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Form
```
写起来基本上就是把`C++`的函数换成`py`，其他完全不变

## 0x03.后记
不知道怎么实现之前一脸懵逼，
看到例程怎么实现的豁然开朗（

## 0x04.引用
[.NET 爱python——pythonnet模块使用](https://blog.csdn.net/qq_27825451/article/details/102307558)