!macro customHeader
    !system "echo '' > ${BUILD_RESOURCES_DIR}/customHeader"
!macroend

!macro customInstall
    MessageBox MB_OK "感谢您安装 BiliBili History Frontend！"
!macroend

!macro customUnInstall
    MessageBox MB_OK "BiliBili History Frontend 已成功卸载。"
!macroend
