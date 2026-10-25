<template>
  <div class="min-h-screen bg-gray-50/30 dark:bg-gray-900">
    <div class="py-2 md:py-4">
      <div class="mx-auto max-w-4xl px-0 md:px-4">
        <!-- 设置导航 -->
        <div class="mb-4 px-3 md:mb-6 md:px-0">
          <div class="border-b border-gray-200 dark:border-gray-700">
            <nav class="-mb-px flex space-x-3 overflow-x-auto md:space-x-6" aria-label="设置选项卡">
              <button
                v-for="(tab, index) in settingTabs"
                :key="index"
                @click="activeTab = tab.key"
                class="flex items-center space-x-1.5 border-b-2 px-1 py-3 text-[13px] font-medium transition-colors md:space-x-2 md:text-sm"
                :class="activeTab === tab.key
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:border-gray-600 dark:hover:text-gray-300'"
              >
                <div class="h-4 w-4 md:h-5 md:w-5" v-html="tab.icon"></div>
                <span>{{ tab.label }}</span>
              </button>
            </nav>
          </div>
        </div>

        <!-- 设置内容 -->
        <div class="space-y-4">
          <!-- 基础设置 -->
          <section v-if="activeTab === 'basic'">
            <div class="divide-y divide-gray-200 border-y border-gray-200 bg-white dark:divide-gray-700 dark:border-gray-700 dark:bg-gray-800 md:rounded-lg md:border md:border-x">
              <!-- 服务器配置 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="mb-2.5 flex items-center justify-between md:mb-3">
                  <div>
                    <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">服务器配置</h3>
                    <p class="mt-0.5 text-xs text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">配置API服务器地址，修改后将自动刷新页面</p>
                  </div>
                </div>
                <div class="flex gap-2">
                  <input
                    v-model="serverUrl"
                    type="text"
                    class="block min-w-0 flex-1 rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 text-[11px] md:text-sm"
                    placeholder="例如：http://localhost:8899"
                  />
                  <div class="flex shrink-0 gap-1.5 md:gap-2">
                    <button
                      @click="resetServerUrl"
                      class="inline-flex items-center justify-center rounded-lg bg-[#fb7299]/5 px-2.5 py-2 text-[11px] font-medium text-[#fb7299] md:text-sm hover:bg-[#fb7299]/10 dark:bg-[#fb7299]/10 dark:hover:bg-[#fb7299]/20 md:px-3"
                    >
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                    </button>
                    <button
                      @click="saveServerUrl"
                      class="inline-flex items-center justify-center rounded-lg bg-[#fb7299] px-3 py-2 text-[11px] font-medium text-white md:text-sm hover:bg-[#fb7299]/90 md:px-4"
                    >
                      保存
                    </button>
                  </div>
                </div>
              </div>

              <!-- MCP配置 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="flex items-start justify-between gap-3">
                  <div class="min-w-0 flex-1">
                    <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">MCP局域网只读服务</h3>
                    <p class="mt-0.5 text-[10px] text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">允许其他AI客户端通过MCP读取本地历史记录，开关保存后立即生效</p>
                  </div>
                  <label
                    class="relative inline-flex shrink-0 items-center"
                    :class="(isMcpConfigLoading || isMcpConfigSaving || !mcpConfigAvailable) ? 'cursor-not-allowed opacity-60' : 'cursor-pointer'"
                  >
                    <input
                      type="checkbox"
                      v-model="mcpConfig.enabled"
                      class="peer sr-only"
                      :disabled="isMcpConfigLoading || isMcpConfigSaving || !mcpConfigAvailable"
                      @change="handleMcpEnabledChange"
                    >
                    <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:translate-x-0 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-[#fb7299] peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 dark:bg-gray-600"></div>
                  </label>
                </div>

                <div v-if="mcpConfigAvailable" class="mt-3 space-y-3">
                  <div class="grid grid-cols-1 gap-3 md:grid-cols-2">
                    <div>
                      <label class="mb-1 block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm">MCP URL</label>
                      <div class="flex gap-2">
                        <input
                          :value="mcpUrl"
                          readonly
                          type="text"
                          class="block min-w-0 flex-1 rounded-md border-gray-300 bg-gray-50 text-[11px] shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] dark:border-gray-600 dark:bg-gray-900 dark:text-gray-100 md:text-sm"
                        />
                        <button
                          @click="copyText(mcpUrl, 'MCP URL')"
                          class="inline-flex shrink-0 items-center justify-center rounded-lg bg-[#fb7299]/5 px-2.5 py-2 text-[11px] font-medium text-[#fb7299] hover:bg-[#fb7299]/10 dark:bg-[#fb7299]/10 dark:hover:bg-[#fb7299]/20 md:text-sm"
                          title="复制MCP URL"
                        >
                          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                          </svg>
                        </button>
                      </div>
                    </div>

                    <div>
                      <label class="mb-1 block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm">Bearer Token</label>
                      <div class="flex gap-2">
                        <input
                          :value="mcpConfig.token"
                          readonly
                          type="password"
                          class="block min-w-0 flex-1 rounded-md border-gray-300 bg-gray-50 text-[11px] shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] dark:border-gray-600 dark:bg-gray-900 dark:text-gray-100 md:text-sm"
                          placeholder="未配置Token"
                        />
                        <button
                          @click="copyText(mcpConfig.token, 'Bearer Token')"
                          :disabled="!mcpConfig.token"
                          class="inline-flex shrink-0 items-center justify-center rounded-lg bg-[#fb7299]/5 px-2.5 py-2 text-[11px] font-medium text-[#fb7299] hover:bg-[#fb7299]/10 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-[#fb7299]/10 dark:hover:bg-[#fb7299]/20 md:text-sm"
                          title="复制Bearer Token"
                        >
                          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>

                  <div>
                    <div class="mb-1 flex items-center justify-between gap-2">
                      <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm">AI连接提示词</label>
                      <button
                        @click="copyText(mcpConnectionPrompt, 'AI连接提示词')"
                        class="inline-flex shrink-0 items-center rounded-lg bg-[#fb7299]/5 px-2.5 py-1.5 text-[11px] font-medium text-[#fb7299] hover:bg-[#fb7299]/10 dark:bg-[#fb7299]/10 dark:hover:bg-[#fb7299]/20 md:text-sm"
                      >
                        <svg class="mr-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                        复制提示词
                      </button>
                    </div>
                    <textarea
                      :value="mcpConnectionPrompt"
                      readonly
                      rows="9"
                      class="block w-full resize-y rounded-md border-gray-300 bg-gray-50 text-[11px] leading-5 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] dark:border-gray-600 dark:bg-gray-900 dark:text-gray-100 md:text-sm"
                    ></textarea>
                  </div>

                  <div>
                    <div class="mb-1 flex items-center justify-between gap-2">
                      <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm">配套 Skill</label>
                      <button
                        @click="copyText(mcpConfig.skill_content, '配套 Skill')"
                        :disabled="!mcpConfig.skill_content"
                        class="inline-flex shrink-0 items-center rounded-lg bg-[#fb7299]/5 px-2.5 py-1.5 text-[11px] font-medium text-[#fb7299] hover:bg-[#fb7299]/10 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-[#fb7299]/10 dark:hover:bg-[#fb7299]/20 md:text-sm"
                      >
                        <svg class="mr-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                        复制 Skill
                      </button>
                    </div>
                    <textarea
                      :value="mcpConfig.skill_content || '后端未找到配套 Skill 文件'"
                      readonly
                      rows="11"
                      class="block w-full resize-y rounded-md border-gray-300 bg-gray-50 text-[11px] leading-5 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] dark:border-gray-600 dark:bg-gray-900 dark:text-gray-100 md:text-sm"
                    ></textarea>
                  </div>
                </div>

                <p v-else-if="!isMcpConfigLoading" class="mt-2 text-[10px] text-amber-600 dark:text-amber-300 md:text-sm">
                  当前后端暂不支持MCP配置接口，请更新并重启后端后再使用。
                </p>
              </div>

              <!-- 图片源设置 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="flex items-center justify-between gap-3">
                  <div class="flex-1">
                    <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">使用本地图片源</h3>
                    <p class="mt-0.5 text-[10px] text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">选择使用本地图片源或在线图片源，本地图片源适合离线访问</p>
                  </div>
                  <label class="relative inline-flex shrink-0 cursor-pointer items-center">
                    <input type="checkbox" v-model="useLocalImages" class="peer sr-only" @change="handleImageSourceChange">
                    <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:translate-x-0 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-[#fb7299] peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 dark:bg-gray-600"></div>
                  </label>
                </div>
              </div>

              <!-- 隐私模式 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="flex items-center justify-between gap-3">
                  <div class="flex-1">
                    <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">隐私模式</h3>
                    <p class="mt-0.5 text-[10px] text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">开启后将模糊显示标题、封面、UP主名称等敏感信息</p>
                  </div>
                  <label class="relative inline-flex shrink-0 cursor-pointer items-center">
                    <input type="checkbox" v-model="privacyMode" class="peer sr-only">
                    <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:translate-x-0 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-[#fb7299] peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 dark:bg-gray-600"></div>
                  </label>
                </div>
              </div>

              <!-- 侧边栏设置 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="flex items-center justify-between gap-3">
                  <div class="flex-1">
                    <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">侧边栏显示</h3>
                    <p class="mt-0.5 text-[10px] text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">设置是否默认显示侧边栏，关闭后侧边栏将自动收起</p>
                  </div>
                  <label class="relative inline-flex shrink-0 cursor-pointer items-center">
                    <input type="checkbox" v-model="showSidebar" class="peer sr-only" @change="handleSidebarChange">
                    <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:translate-x-0 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-[#fb7299] peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 dark:bg-gray-600"></div>
                  </label>
                </div>
              </div>

              <!-- 首页默认布局设置 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="flex items-center justify-between gap-3">
                  <div class="flex-1">
                    <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">首页默认布局</h3>
                    <p class="mt-0.5 text-[10px] text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">设置历史记录页面的默认展示方式，开启为网格视图，关闭为列表视图</p>
                  </div>
                  <label class="relative inline-flex shrink-0 cursor-pointer items-center">
                    <input type="checkbox" v-model="isGridLayout" class="peer sr-only" @change="handleLayoutChange">
                    <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:translate-x-0 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-[#fb7299] peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 dark:bg-gray-600"></div>
                  </label>
                </div>
              </div>

              <!-- 同步已删除记录 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="flex items-center justify-between gap-3">
                  <div class="flex-1">
                    <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">同步已删除记录</h3>
                    <p class="mt-0.5 text-[10px] text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">开启后将同步已删除的历史记录，建议仅在需要恢复记录时开启</p>
                  </div>
                  <label class="relative inline-flex shrink-0 cursor-pointer items-center">
                    <input type="checkbox" v-model="syncDeleted" class="peer sr-only">
                    <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:translate-x-0 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-[#fb7299] peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 dark:bg-gray-600"></div>
                  </label>
                </div>
              </div>

              <!-- 同步删除B站历史记录 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="flex items-center justify-between gap-3">
                  <div class="flex-1">
                    <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">同步删除B站历史记录</h3>
                    <p class="mt-0.5 text-[10px] text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">开启后删除本地历史记录时，同时删除B站服务器上的对应记录</p>
                  </div>
                  <label class="relative inline-flex shrink-0 cursor-pointer items-center">
                    <input type="checkbox" v-model="syncDeleteToBilibili" class="peer sr-only" @change="handleSyncDeleteToBilibiliChange">
                    <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:translate-x-0 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-[#fb7299] peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 dark:bg-gray-600"></div>
                  </label>
                </div>
              </div>

              <!-- 启动时数据完整性校验 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="flex items-center justify-between gap-3">
                  <div class="flex-1">
                    <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">启动时数据完整性校验</h3>
                    <p class="mt-0.5 text-[10px] text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">开启后每次启动应用时都会进行数据完整性校验，关闭可加快启动速度</p>
                  </div>
                  <label class="relative inline-flex shrink-0 cursor-pointer items-center">
                    <input type="checkbox" v-model="checkIntegrityOnStartup" class="peer sr-only" @change="handleIntegrityCheckChange">
                    <div class="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-5 after:w-5 after:translate-x-0 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-[#fb7299] peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 dark:bg-gray-600"></div>
                  </label>
                </div>
              </div>

              <!-- 邮件配置 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="flex items-center justify-between mb-2">
                  <h3 class="text-[14px] font-medium text-gray-900 dark:text-gray-100 md:text-base">邮件配置</h3>
                  <div class="flex space-x-2">
                    <button
                      @click="resetEmailConfig"
                      class="inline-flex items-center px-3 py-1.5 text-[11px] font-medium text-[#fb7299] md:text-sm bg-[#fb7299]/5 dark:bg-[#fb7299]/10 rounded-lg hover:bg-[#fb7299]/10 dark:hover:bg-[#fb7299]/20"
                    >
                      <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      重置
                    </button>
                    <button
                      @click="saveEmailConfig"
                      class="inline-flex items-center px-3 py-1.5 text-[11px] font-medium text-white md:text-sm bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90"
                    >
                      保存
                    </button>
                    <button
                      @click="testEmailConfig"
                      class="inline-flex items-center px-3 py-1.5 text-[11px] font-medium text-white md:text-sm bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90"
                      :disabled="!isEmailConfigComplete"
                    >
                      <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 19v-8.93a2 2 0 01.89-1.664l7-4.666a2 2 0 012.22 0l7 4.666A2 2 0 0121 10.07V19M3 19a2 2 0 002 2h14a2 2 0 002-2M3 19l6.75-4.5M21 19l-6.75-4.5M3 10l6.75 4.5M21 10l-6.75 4.5m0 0l-1.14.76a2 2 0 01-2.22 0l-1.14-.76" />
                      </svg>
                      测试
                    </button>
                  </div>
                </div>

                <div class="mt-2 grid grid-cols-1 gap-3 md:grid-cols-2">
                  <div class="space-y-3">
                    <div>
                      <label class="mb-1 block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm">SMTP服务器</label>
                      <input
                        v-model="emailConfig.smtp_server"
                        type="text"
                        class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                        placeholder="smtp.qq.com"
                      />
                    </div>
                    <div>
                      <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm mb-1">发件人邮箱</label>
                      <input
                        v-model="emailConfig.sender"
                        type="email"
                        class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                        placeholder="example@qq.com"
                      />
                    </div>
                    <div>
                      <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm mb-1">收件人邮箱</label>
                      <input
                        v-model="emailConfig.receiver"
                        type="email"
                        class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                        placeholder="receiver@qq.com"
                      />
                    </div>
                  </div>
                  <div class="space-y-3">
                    <div>
                      <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm mb-1">SMTP端口</label>
                      <input
                        v-model.number="emailConfig.smtp_port"
                        type="number"
                        class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                        placeholder="587"
                      />
                    </div>
                    <div>
                      <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm mb-1">SMTP认证用户名（可选）</label>
                      <input
                        v-model="emailConfig.auth_username"
                        type="text"
                        class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                        placeholder="为空则使用发件人邮箱"
                      />
                      <p class="mt-1 text-[10px] text-gray-500 dark:text-gray-400 md:text-xs">
                        QQ邮箱通常留空；Resend等服务可填写独立认证用户名。
                      </p>
                    </div>
                    <div>
                      <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm mb-1">邮箱授权码</label>
                      <input
                        v-model="emailConfig.password"
                        type="password"
                        class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                        placeholder="授权码"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- Apprise推送配置 -->
          <section v-if="activeTab === 'basic'">
            <div class="divide-y divide-gray-200 border-y border-gray-200 bg-white dark:divide-gray-700 dark:border-gray-700 dark:bg-gray-800 md:rounded-lg md:border md:border-x">
              <ApriseSettings />
            </div>
          </section>

          <!-- 数据管理 -->
          <section v-if="activeTab === 'data'">
            <div class="divide-y divide-gray-200 border-y border-gray-200 bg-white dark:divide-gray-700 dark:border-gray-700 dark:bg-gray-800 md:rounded-lg md:border md:border-x">
              <!-- 数据导出 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div>
                  <div class="mb-3 flex items-center justify-between md:mb-4">
                    <div>
                      <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">数据导出</h3>
                      <p class="mt-0.5 text-[10px] text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">导出历史记录数据到Excel文件，支持按年份、月份或日期范围导出</p>
                    </div>
                  </div>

                  <!-- 导出选项 -->
                  <div class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 p-4 rounded-lg">
                    <div class="flex flex-wrap items-end gap-4">
                      <!-- 年份选择 (始终显示) -->
                      <div class="w-32">
                        <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm mb-1">年份</label>
                        <select
                          v-model="exportOptions.year"
                          class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                        >
                          <option v-for="year in availableYears" :key="year" :value="year">
                            {{ year }}年
                          </option>
                        </select>
                      </div>

                      <!-- 导出类型选择 -->
                      <div class="w-40">
                        <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm mb-1">导出类型</label>
                        <select
                          v-model="exportOptions.exportType"
                          class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                        >
                          <option value="year">全年数据</option>
                          <option value="month">按月份</option>
                          <option value="dateRange">按日期范围</option>
                        </select>
                      </div>

                      <!-- 按月选择框 -->
                      <div v-if="exportOptions.exportType === 'month'" class="w-24">
                        <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm mb-1">月份</label>
                        <select
                          v-model="exportOptions.month"
                          class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                        >
                          <option v-for="month in 12" :key="month" :value="month">
                            {{ month }}月
                          </option>
                        </select>
                      </div>

                      <!-- 日期范围选择框 -->
                      <template v-if="exportOptions.exportType === 'dateRange'">
                        <div class="w-40">
                          <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm mb-1">开始日期</label>
                          <input
                            type="date"
                            v-model="exportOptions.startDate"
                            class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                          />
                        </div>

                        <div class="w-40">
                          <label class="block text-[12px] font-medium text-gray-700 dark:text-gray-300 md:text-sm mb-1">结束日期</label>
                          <input
                            type="date"
                            v-model="exportOptions.endDate"
                            class="block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-[11px] md:text-sm"
                          />
                        </div>
                      </template>

                      <!-- 导出按钮 -->
                      <button
                        @click="exportAndDownloadExcel"
                        :disabled="isExporting"
                        class="inline-flex items-center px-4 py-2 text-[11px] font-medium text-white md:text-sm bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90 disabled:opacity-50 h-10"
                      >
                        <svg v-if="isExporting" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        {{ isExporting ? '导出中...' : '导出Excel' }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 数据库下载 -->
              <div class="p-3 transition-colors duration-200 hover:bg-gray-50 dark:hover:bg-gray-700 md:p-4">
                <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h3 class="text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">数据库下载</h3>
                    <p class="mt-0.5 text-[10px] text-gray-500 dark:text-gray-400 md:mt-0 md:text-sm">下载完整的SQLite数据库文件，包含所有历史记录数据</p>
                  </div>
                  <button
                    @click="downloadSqlite"
                    class="inline-flex w-full justify-center items-center sm:w-auto px-4 py-2 text-[11px] font-medium text-white md:text-sm bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90"
                  >
                    <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    下载SQLite数据库
                  </button>
                </div>
              </div>
            </div>

            <!-- 危险操作 -->
            <div class="mt-4">
              <div class="border-y border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800 md:rounded-lg md:border md:border-x">
                <div class="p-3 transition-colors duration-200 hover:bg-red-50 dark:hover:bg-red-900/20 md:p-4 md:rounded-lg">
                  <h3 class="mb-2 text-[13px] font-medium text-gray-900 dark:text-gray-100 md:text-base">危险操作</h3>
                  <div class="flex items-center justify-between p-2 border border-red-100 dark:border-red-900/40 rounded-lg bg-red-50 dark:bg-red-900/10">
                    <div>
                      <h4 class="text-sm font-medium text-red-700 dark:text-red-300">数据库重置</h4>
                      <p class="text-xs text-red-600 dark:text-red-300">删除现有数据库并重新导入数据（此操作不可逆）</p>
                    </div>
                    <button
                      @click="handleResetDatabase"
                      class="inline-flex items-center px-3 py-1.5 text-[11px] font-medium text-white md:text-sm bg-red-500 rounded-lg hover:bg-red-600"
                    >
                      <svg class="mr-1.5 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      重置数据库
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </section>



          <!-- 关于页面 -->
          <section v-if="activeTab === 'about'">
            <div class="border-y border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-800 md:rounded-lg md:border md:border-x md:p-6">
              <!-- 页面标题 -->
              <div class="mb-4 md:mb-6">
                <h1 class="flex items-center text-sm font-bold text-gray-800 dark:text-gray-100 md:text-2xl">
                  <span class="bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">关于本项目</span>
                </h1>
                <p class="mt-1 text-[10px] text-gray-500 dark:text-gray-400 md:mt-2 md:text-sm">哔哩哔哩历史记录管理与分析工具</p>
              </div>

              <!-- 项目介绍卡片 -->
              <div class="mb-5 md:mb-6">
                <h2 class="mb-2 flex items-center text-[13px] font-medium text-gray-800 dark:text-gray-100 md:mb-4 md:text-xl">
                  <svg class="mr-1.5 h-3.5 w-3.5 text-[#fb7299] md:mr-2 md:h-5 md:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  项目简介
                </h2>
                <div class="space-y-2 text-[11px] text-gray-600 dark:text-gray-300 md:space-y-3 md:text-sm">
                  <p>
                    此项目是一个哔哩哔哩历史记录管理与分析工具，帮助用户更好地管理和分析自己的B站观看历史。基于Vue 3构建，通过现代的界面设计提供强大的功能，包括历史记录查询、视频下载、数据分析等多项功能。
                  </p>

                  <div class="mt-3 space-y-2 md:mt-4 md:space-y-3">
                    <div class="flex items-center">
                      <svg class="mr-1.5 h-3.5 w-3.5 text-[#fb7299] md:mr-2 md:h-5 md:w-5" fill="currentColor" viewBox="0 0 24 24">
                        <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
                      </svg>
                      <span class="w-16 shrink-0 text-gray-500 md:w-24">前端项目</span>
                      <a href="https://github.com/2977094657/BiliHistoryFrontend" target="_blank" rel="noopener noreferrer" class="break-all text-[#fb7299] hover:underline">https://github.com/2977094657/BiliHistoryFrontend</a>
                    </div>
                    <div class="flex items-center">
                      <svg class="mr-1.5 h-3.5 w-3.5 text-[#fb7299] md:mr-2 md:h-5 md:w-5" fill="currentColor" viewBox="0 0 24 24">
                        <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
                      </svg>
                      <span class="w-16 shrink-0 text-gray-500 md:w-24">后端项目</span>
                      <a href="https://github.com/2977094657/BilibiliHistoryFetcher" target="_blank" rel="noopener noreferrer" class="break-all text-[#fb7299] hover:underline">https://github.com/2977094657/BilibiliHistoryFetcher</a>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 技术致谢卡片 -->
              <div>
                <h2 class="mb-2 flex items-center text-[13px] font-medium text-gray-800 dark:text-gray-100 md:mb-4 md:text-xl">
                  <svg class="mr-1.5 h-3.5 w-3.5 text-[#fb7299] md:mr-2 md:h-5 md:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                  技术致谢
                </h2>

                <div class="mt-2 space-y-2 text-[11px] text-gray-600 dark:text-gray-300 md:mt-4 md:space-y-4 md:text-sm">
                  <ul class="list-disc space-y-1.5 pl-4 md:space-y-2 md:pl-5">
                    <li><a href="https://github.com/SocialSisterYi/bilibili-API-collect" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline">bilibili-API-collect</a> - 没有它就没有这个项目</li>
                    <li><a href="https://yutto.nyakku.moe/" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline">Yutto</a> - 可爱的B站视频下载工具</li>
                    <li><a href="https://github.com/zhw2590582/ArtPlayer" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline">ArtPlayer</a> - 强大且灵活的HTML5视频播放器</li>
                    <li><a href="https://www.aicu.cc/" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline">aicu.cc</a> - 第三方B站用户评论API</li>
                    <li>所有贡献者</li>
                  </ul>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { showNotify } from 'vant'
import 'vant/es/notify/style'
import 'vant/es/toast/style'
import 'vant/es/dialog/style'
import {
  exportHistory,
  downloadExcelFile,
  downloadDatabase,
  resetDatabase,
  getAvailableYears,
  importSqliteData,
  getEmailConfig,
  updateEmailConfig,
  getMcpConfig,
  updateMcpConfig,
  testEmailConfig as testEmailApi,
  getIntegrityCheckConfig,
  updateIntegrityCheckConfig
} from '../../api/api'
import ApriseSettings from './ApriseSettings.vue'
import { setBaseUrl, getCurrentBaseUrl } from '../../api/api'
import { usePrivacyStore } from '../../store/privacy'
import { showDialog } from 'vant'
import { useRoute } from 'vue-router'
import privacyManager from '../../utils/privacyManager'

// 设置选项卡
const settingTabs = [
  {
    key: 'basic',
    label: '基础设置',
    icon: '<svg class="text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2m-2-4h.01M17 16h.01" /></svg>'
  },
  {
    key: 'data',
    label: '数据管理',
    icon: '<svg class="text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" /></svg>'
  },
  {
    key: 'about',
    label: '关于',
    icon: '<svg class="text-[#4D6BFE]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>'
  }
]

const route = useRoute()
const activeTab = ref('basic')

// 监听路由参数变化，切换标签页
watch(() => route.query.tab, (newTab) => {
  if (newTab && settingTabs.some(tab => tab.key === newTab)) {
    activeTab.value = newTab
  }
}, { immediate: true })

const availableYears = ref([])
const isExporting = ref(false)

// 导出选项
const exportOptions = ref({
  year: new Date().getFullYear(),
  month: null,
  startDate: '',
  endDate: '',
  exportType: 'year' // 默认导出全年数据
})
const serverUrl = ref('')
const useLocalImages = ref(localStorage.getItem('useLocalImages') === 'true')
const DEFAULT_EMAIL_CONFIG = {
  smtp_server: 'smtp.qq.com',
  smtp_port: 587,
  sender: '',
  auth_username: '',
  password: '',
  receiver: ''
}
const emailConfig = ref({ ...DEFAULT_EMAIL_CONFIG })

const DEFAULT_MCP_CONFIG = {
  enabled: false,
  path: '/mcp',
  auth_enabled: true,
  token: '',
  token_configured: false,
  max_page_size: 100,
  server_url: '',
  mcp_url: '',
  skill_content: '',
  restart_required: false
}
const mcpConfig = ref({ ...DEFAULT_MCP_CONFIG })
const mcpConfigAvailable = ref(false)
const isMcpConfigLoading = ref(true)
const isMcpConfigSaving = ref(false)

const trimTrailingSlash = (value) => (value || '').trim().replace(/\/+$/, '')

const normalizeMcpPath = (path) => {
  let normalizedPath = (path || '/mcp').trim()
  if (!normalizedPath.startsWith('/')) {
    normalizedPath = `/${normalizedPath}`
  }
  if (normalizedPath.length > 1) {
    normalizedPath = normalizedPath.replace(/\/+$/, '')
  }
  return normalizedPath || '/mcp'
}

const mcpUrl = computed(() => {
  const baseUrl = trimTrailingSlash(serverUrl.value || mcpConfig.value.server_url || getCurrentBaseUrl())
  const path = normalizeMcpPath(mcpConfig.value.path)
  return path === '/' ? `${baseUrl}/` : `${baseUrl}${path}/`
})

const mcpConnectionPrompt = computed(() => {
  const authLine = mcpConfig.value.auth_enabled
    ? `Authorization: Bearer ${mcpConfig.value.token || '<token>'}`
    : 'Authorization: not required'

  return [
    '请通过 MCP Streamable HTTP 连接我的 BilibiliHistoryFetcher 只读服务。',
    '',
    `MCP URL: ${mcpUrl.value}`,
    authLine,
    '',
    '连接后请先读取以下 Resources：',
    '- bili://project/overview',
    '- bili://project/data-status',
    '- bili://project/tool-guide',
    '',
    '使用规则：',
    '- 这是只读 MCP，不要请求同步、下载、删除、登录、重置数据库或修改配置。',
    '- 查询明细时必须分页，优先使用统计/摘要工具，再按需读取 records。',
    '- 观看历史属于隐私数据，只在当前任务需要时读取。'
  ].join('\n')
})

// 隐私模式
const { isPrivacyMode, setPrivacyMode } = usePrivacyStore()
const privacyMode = ref(isPrivacyMode.value)

// 同步已删除记录
const syncDeleted = ref(localStorage.getItem('syncDeleted') === 'true')

// 监听同步已删除记录变化
watch(syncDeleted, (newVal) => {
  localStorage.setItem('syncDeleted', newVal.toString())
  showNotify({
    type: 'success',
    message: newVal ? '已开启同步已删除记录' : '已关闭同步已删除记录'
  })
})

// 同步删除B站历史记录
const syncDeleteToBilibili = ref(localStorage.getItem('syncDeleteToBilibili') === 'true')

// 处理同步删除B站历史记录变更
const handleSyncDeleteToBilibiliChange = () => {
  localStorage.setItem('syncDeleteToBilibili', syncDeleteToBilibili.value.toString())
  showNotify({
    type: 'success',
    message: syncDeleteToBilibili.value ? '已开启同步删除B站历史记录' : '已关闭同步删除B站历史记录'
  })
}

// 启动时数据完整性校验
const checkIntegrityOnStartup = ref(true)

// 处理数据完整性校验设置变更
const handleIntegrityCheckChange = async () => {
  try {
    const response = await updateIntegrityCheckConfig(checkIntegrityOnStartup.value)
    if (response.data && response.data.success) {
      showNotify({
        type: 'success',
        message: checkIntegrityOnStartup.value ? '已开启启动时数据完整性校验' : '已关闭启动时数据完整性校验'
      })
    } else {
      throw new Error(response.data?.message || '更新配置失败')
    }
  } catch (error) {
    console.error('更新数据完整性校验配置失败:', error)
    showNotify({
      type: 'danger',
      message: `更新配置失败: ${error.message}`
    })
    // 恢复原值
    checkIntegrityOnStartup.value = !checkIntegrityOnStartup.value
  }
}

// 首页默认布局设置 - 网格布局或列表布局
const isGridLayout = ref(localStorage.getItem('defaultLayout') === 'list' ? false : true) // 默认为网格视图





// 处理布局变更
const handleLayoutChange = () => {
  // 更新localStorage，保存用户选择的布局模式
  const newLayout = isGridLayout.value ? 'grid' : 'list'
  localStorage.setItem('defaultLayout', newLayout)

  // 触发全局事件，通知其他组件更新布局
  try {
    const event = new CustomEvent('layout-setting-changed', {
      detail: { layout: newLayout }
    })
    window.dispatchEvent(event)
    console.log('已触发布局设置更新事件:', newLayout)
  } catch (error) {
    console.error('触发布局设置更新事件失败:', error)
  }

  showNotify({
    type: 'success',
    message: `已切换到${isGridLayout.value ? '网格' : '列表'}视图`
  })
}

// 监听隐私模式变化
watch(privacyMode, (newVal) => {
  // 更新store中的隐私模式状态
  setPrivacyMode(newVal)

  // 更新localStorage中的隐私模式状态并触发自定义事件
  if (newVal) {
    privacyManager.enable()

  } else {
    privacyManager.disable()
  }
})

// 侧边栏显示设置
const showSidebar = ref(localStorage.getItem('showSidebar') !== 'false') // 默认为true

// 处理侧边栏设置变更
const handleSidebarChange = () => {
  localStorage.setItem('showSidebar', showSidebar.value.toString())

  // 触发全局事件，通知侧边栏组件更新设置
  try {
    const event = new CustomEvent('sidebar-setting-changed', {
      detail: { showSidebar: showSidebar.value }
    })
    window.dispatchEvent(event)
    console.log('已触发侧边栏设置更新事件:', showSidebar.value)
  } catch (error) {
    console.error('触发侧边栏设置更新事件失败:', error)
  }

  showNotify({
    type: 'success',
    message: `已${showSidebar.value ? '启用' : '禁用'}侧边栏显示`
  })
}

// 初始化服务器地址
onMounted(async () => {
  console.log('Settings组件开始挂载')

  // 添加隐私模式监听器
  privacyManager.addListener((isEnabled) => {
    console.log('Settings组件接收到隐私模式变化:', isEnabled)

    // 更新组件内的隐私模式状态
    if (privacyMode.value !== isEnabled) {
      privacyMode.value = isEnabled
    }

  })

  // 同步当前隐私模式状态
  const currentPrivacyMode = privacyManager.isEnabled()
  if (privacyMode.value !== currentPrivacyMode) {
    privacyMode.value = currentPrivacyMode
  }


  try {
    serverUrl.value = getCurrentBaseUrl()
    console.log('当前服务器地址:', serverUrl.value)


    // 监听侧边栏切换事件
    window.addEventListener('sidebar-toggle-changed', handleSidebarToggleEvent)

    // 监听布局切换事件
    window.addEventListener('layout-changed', handleLayoutChangedEvent)

    // 获取可用年份数据
    await getAvailableYears().then(response => {
      if (response.data.status === 'success') {
        availableYears.value = response.data.data
        if (availableYears.value.length > 0) {
          exportOptions.value.year = availableYears.value[0]
        }
      }
    }).catch(error => {
      console.error('获取可用年份失败:', error)
    })

    await Promise.all([
      (async () => {
        console.log('开始初始化邮件配置')
        await initEmailConfig()
        console.log('邮件配置初始化完成')
      })(),
      (async () => {
        console.log('开始初始化MCP配置')
        await initMcpConfig()
        console.log('MCP配置初始化完成')
      })(),
      (async () => {
        console.log('开始获取可用年份')
        try {
          const response = await getAvailableYears()
          console.log('获取年份响应:', response.data)
          if (response.data.status === 'success') {
            availableYears.value = response.data.data.sort((a, b) => b - a)
            if (availableYears.value.length > 0) {
              // 设置导出选项的年份
              exportOptions.value.year = availableYears.value[0]
            }
            console.log('获取可用年份成功:', availableYears.value)
          } else {
            throw new Error(response.data.message || '获取年份列表失败')
          }
        } catch (error) {
          console.error('获取可用年份失败:', error)
          showNotify({
            type: 'danger',
            message: '获取年份列表失败'
          })
          // 设置当前年份作为默认值
          const currentYear = new Date().getFullYear()
          availableYears.value = [currentYear]

          // 重置导出选项
          exportOptions.value = {
            year: currentYear,
            month: null,
            startDate: '',
            endDate: '',
            exportType: 'year'
          }
        }
      })(),
      (async () => {
        console.log('开始获取数据完整性校验配置')
        try {
          const response = await getIntegrityCheckConfig()
          if (response.data && response.data.success) {
            checkIntegrityOnStartup.value = response.data.check_on_startup
            console.log('数据完整性校验配置获取成功:', checkIntegrityOnStartup.value)
          } else {
            throw new Error(response.data?.message || '获取配置失败')
          }
        } catch (error) {
          console.error('获取数据完整性校验配置失败:', error)
          // 使用默认值
          checkIntegrityOnStartup.value = true
        }
        console.log('数据完整性校验配置获取完成')
      })()
    ])
    console.log('Settings组件初始化完成')
  } catch (error) {
    console.error('Settings组件初始化失败:', error)
  }
})

// 导出并下载Excel
const exportAndDownloadExcel = async () => {
  if (isExporting.value) return

  try {
    // 准备导出参数
    let exportParams = {}

    // 根据导出类型设置参数
    switch (exportOptions.value.exportType) {
      case 'month':
        // 检查月份是否选择
        if (!exportOptions.value.month) {
          showNotify({
            type: 'danger',
            message: '请选择要导出的月份'
          })
          return
        }
        exportParams = {
          year: exportOptions.value.year,
          month: exportOptions.value.month
        }
        break

      case 'dateRange':
        // 验证日期范围
        if (!exportOptions.value.startDate || !exportOptions.value.endDate) {
          showNotify({
            type: 'danger',
            message: '请选择完整的日期范围'
          })
          return
        }

        const startDate = new Date(exportOptions.value.startDate)
        const endDate = new Date(exportOptions.value.endDate)
        if (startDate > endDate) {
          showNotify({
            type: 'danger',
            message: '开始日期不能晚于结束日期'
          })
          return
        }

        // 只传递日期范围参数，不传递年份参数
        exportParams = {
          start_date: exportOptions.value.startDate,
          end_date: exportOptions.value.endDate
        }
        break

      case 'year':
      default:
        // 全年数据，只需要year参数
        exportParams = {
          year: exportOptions.value.year
        }
        break
    }

    isExporting.value = true
    showNotify({
      type: 'primary',
      message: '正在导出数据...'
    })

    console.log('导出选项:', exportParams)
    const response = await exportHistory(exportParams)
    console.log('导出响应:', response.data)

    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: '导出成功，准备下载...'
      })

      // 使用响应中的文件名
      const filename = response.data.filename
      console.log('准备下载文件:', filename)
      await downloadExcelFile(filename)
      showNotify({
        type: 'success',
        message: '下载完成'
      })
    } else {
      throw new Error(response.data.message)
    }
  } catch (error) {
    console.error('导出错误:', error)
    let errorMessage = error.message

    // 尝试获取服务器返回的错误信息
    if (error.response && error.response.data) {
      if (error.response.data.detail) {
        errorMessage = error.response.data.detail
      } else if (typeof error.response.data === 'string') {
        errorMessage = error.response.data
      }
    }

    showNotify({
      type: 'danger',
      message: `操作失败：${errorMessage}`
    })
  } finally {
    isExporting.value = false
  }
}

// 下载SQLite数据库
const downloadSqlite = async () => {
  try {
    await downloadDatabase()
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `下载失败：${error.message}`
    })
  }
}

// 保存服务器地址
const saveServerUrl = () => {
  try {
    // 简单的URL格式验证
    const url = new URL(serverUrl.value)
    setBaseUrl(serverUrl.value)
    showNotify({
      type: 'success',
      message: '服务器地址已更新，页面即将刷新'
    })
  } catch (error) {
    showNotify({
      type: 'danger',
      message: '请输入有效的URL地址'
    })
  }
}

// 在script setup部分添加重置功能
const FALLBACK_DEFAULT_SERVER_URL = 'http://localhost:8899';
const DEFAULT_SERVER_URL = import.meta.env.VITE_DEFAULT_BACKEND_URL || FALLBACK_DEFAULT_SERVER_URL;

// 重置服务器地址
const resetServerUrl = () => {
  showDialog({
    title: '重置服务器地址',
    message: '确定要将服务器地址重置为默认值吗？',
    showCancelButton: true,
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    confirmButtonColor: '#fb7299'
  }).then((result) => {
    if (result === 'confirm') {
      serverUrl.value = DEFAULT_SERVER_URL
      setBaseUrl(DEFAULT_SERVER_URL)
      showNotify({
        type: 'success',
        message: '服务器地址已重置，页面即将刷新'
      })
    }
  })
}

// 处理数据库重置
const handleResetDatabase = () => {
  showDialog({
    title: '危险操作确认',
    message: '此操作将删除现有数据库并重新导入数据。此操作不可逆，确定要继续吗？',
    showCancelButton: true,
    confirmButtonText: '确定重置',
    cancelButtonText: '取消',
    confirmButtonColor: '#dc2626'
  }).then(async (result) => {
    if (result === 'confirm') {
      try {
        showNotify({
          type: 'warning',
          message: '正在重置数据库...'
        })

        // 重置数据库
        const resetResponse = await resetDatabase()
        if (resetResponse.data.status === 'success') {
          showNotify({
            type: 'success',
            message: '数据库已重置，正在重新导入数据...'
          })

          // 重新导入数据
          try {
            const importResponse = await importSqliteData()
            if (importResponse.data.status === 'success') {
              showNotify({
                type: 'success',
                message: '数据导入完成，页面即将刷新'
              })
              // 等待1秒后刷新页面，确保用户看到成功提示
              setTimeout(() => {
                window.location.reload()
              }, 1000)
            } else {
              throw new Error(importResponse.data.message || '数据导入失败')
            }
          } catch (importError) {
            showNotify({
              type: 'danger',
              message: `数据导入失败：${importError.message}`
            })
          }
        }
      } catch (error) {
        showNotify({
          type: 'danger',
          message: `重置失败：${error.message}`
        })
      }
    }
  })
}

// 处理图片源变更
const handleImageSourceChange = () => {
  localStorage.setItem('useLocalImages', useLocalImages.value.toString())
  showNotify({
    type: 'success',
    message: `已${useLocalImages.value ? '启用' : '禁用'}本地图片源`
  })
  // 刷新页面以应用新设置
  window.location.reload()
}

// 初始化邮件配置
const initEmailConfig = async () => {
  try {
    const response = await getEmailConfig()
    if (response.data) {  // 直接检查 response.data
      // 使用解构赋值来更新配置，保留默认值
      emailConfig.value = {
        ...DEFAULT_EMAIL_CONFIG,
        ...response.data  // 直接使用 response.data
      }
    } else {
      emailConfig.value = { ...DEFAULT_EMAIL_CONFIG }
    }
  } catch (error) {
    console.error('获取邮件配置失败:', error)
    showNotify({
      type: 'warning',
      message: '获取邮件配置失败，使用默认配置'
    })
    emailConfig.value = { ...DEFAULT_EMAIL_CONFIG }
  }
}

// 初始化MCP配置
const initMcpConfig = async () => {
  isMcpConfigLoading.value = true
  try {
    const response = await getMcpConfig()
    if (response.data && response.data.status === 'success') {
      mcpConfig.value = {
        ...DEFAULT_MCP_CONFIG,
        ...response.data,
        path: normalizeMcpPath(response.data.path)
      }
      mcpConfigAvailable.value = true
    } else {
      throw new Error(response.data?.message || '获取MCP配置失败')
    }
  } catch (error) {
    console.error('获取MCP配置失败:', error)
    mcpConfig.value = { ...DEFAULT_MCP_CONFIG }
    mcpConfigAvailable.value = false
  } finally {
    isMcpConfigLoading.value = false
  }
}

// 保存MCP开关配置
const handleMcpEnabledChange = async () => {
  if (isMcpConfigSaving.value) return

  const nextEnabled = mcpConfig.value.enabled
  isMcpConfigSaving.value = true

  try {
    const response = await updateMcpConfig({ enabled: nextEnabled })
    if (response.data && response.data.status === 'success') {
      mcpConfig.value = {
        ...mcpConfig.value,
        ...response.data,
        path: normalizeMcpPath(response.data.path)
      }
      mcpConfigAvailable.value = true
      showNotify({
        type: response.data.restart_required ? 'warning' : 'success',
        message: response.data.restart_required ? 'MCP配置已保存，重启后端后生效' : 'MCP配置已保存，已立即生效'
      })
    } else {
      throw new Error(response.data?.message || '保存MCP配置失败')
    }
  } catch (error) {
    console.error('保存MCP配置失败:', error)
    mcpConfig.value.enabled = !nextEnabled
    showNotify({
      type: 'danger',
      message: `保存MCP配置失败：${error.message || '未知错误'}`
    })
  } finally {
    isMcpConfigSaving.value = false
  }
}

const fallbackCopyText = (text) => {
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.setAttribute('readonly', '')
  textarea.style.position = 'fixed'
  textarea.style.left = '-9999px'
  document.body.appendChild(textarea)
  textarea.select()
  const copied = document.execCommand('copy')
  document.body.removeChild(textarea)
  return copied
}

// 复制MCP连接信息
const copyText = async (text, label = '内容') => {
  if (!text) {
    showNotify({
      type: 'warning',
      message: `${label}为空，无法复制`
    })
    return
  }

  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text)
    } else if (!fallbackCopyText(text)) {
      throw new Error('复制失败，请手动复制')
    }
    showNotify({
      type: 'success',
      message: `${label}已复制`
    })
  } catch (error) {
    console.error('复制失败:', error)
    showNotify({
      type: 'danger',
      message: error.message || '复制失败，请手动复制'
    })
  }
}

// 保存邮件配置
const saveEmailConfig = async () => {
  try {
    // 验证邮箱格式
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(emailConfig.value.sender)) {
      throw new Error('发件人邮箱格式不正确')
    }
    if (!emailRegex.test(emailConfig.value.receiver)) {
      throw new Error('收件人邮箱格式不正确')
    }

    // 验证端口号
    if (emailConfig.value.smtp_port < 0 || emailConfig.value.smtp_port > 65535) {
      throw new Error('端口号必须在0-65535之间')
    }

    const response = await updateEmailConfig(emailConfig.value)
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: '邮件配置已保存'
      })
    } else {
      throw new Error(response.data.message || '保存失败')
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `保存失败：${error.message}`
    })
  }
}

// 重置邮件配置
const resetEmailConfig = () => {
  showDialog({
    title: '重置邮件配置',
    message: '确定要重置邮件配置吗？这将清空所有配置并恢复默认的SMTP服务器和端口设置。',
    showCancelButton: true,
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    confirmButtonColor: '#fb7299'
  }).then(async (result) => {
    if (result === 'confirm') {
      try {
        // 完全重置为默认配置
        const resetConfig = { ...DEFAULT_EMAIL_CONFIG }
        emailConfig.value = resetConfig

        // 调用后端API保存重置后的配置
        const response = await updateEmailConfig(resetConfig)
        if (response.data.status === 'success') {
          showNotify({
            type: 'success',
            message: '邮件配置已重置'
          })
        } else {
          throw new Error(response.data.message || '重置失败')
        }
      } catch (error) {
        showNotify({
          type: 'danger',
          message: `重置失败：${error.message}`
        })
        // 如果保存失败，重新获取配置
        await initEmailConfig()
      }
    }
  })
}

// 检查邮件配置是否完整
const isEmailConfigComplete = computed(() => {
  return emailConfig.value.smtp_server &&
         emailConfig.value.smtp_port &&
         emailConfig.value.sender &&
         emailConfig.value.password &&
         emailConfig.value.receiver
})

// 测试邮件配置
const testEmailConfig = async () => {
  try {
    if (!isEmailConfigComplete.value) {
      showNotify({
        type: 'warning',
        message: '请先完善邮件配置'
      })
      return
    }

    // 先保存邮件配置
    try {
      await saveEmailConfig()
    } catch (error) {
      // 如果保存配置失败，则终止测试
      return
    }

    showNotify({
      type: 'primary',
      message: '正在发送测试邮件...'
    })

    const testData = {
      to_email: emailConfig.value.receiver,
      subject: '测试邮件',
      content: '这是一封测试邮件，用于验证邮箱配置是否有效。'
    }

    const response = await testEmailApi(testData)
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: '测试邮件发送成功'
      })
    } else {
      throw new Error(response.data.message || '发送失败')
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `发送失败：${error.message || '未知错误'}`
    })
  }
}

// 处理侧边栏切换事件
const handleSidebarToggleEvent = (event) => {
  if (event.detail && typeof event.detail.showSidebar === 'boolean') {
    showSidebar.value = event.detail.showSidebar
  }
}

// 在script setup部分添加卸载功能
onUnmounted(() => {
  // 移除事件监听
  window.removeEventListener('sidebar-toggle-changed', handleSidebarToggleEvent)
  window.removeEventListener('layout-changed', handleLayoutChangedEvent)
})

// 处理布局变更事件 - 从首页接收的布局变化
const handleLayoutChangedEvent = (event) => {
  if (event.detail && typeof event.detail.layout === 'string') {
    isGridLayout.value = event.detail.layout === 'grid'
  }
}
</script>
