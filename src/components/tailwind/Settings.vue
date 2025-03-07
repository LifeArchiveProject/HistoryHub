<template>
  <div class="min-h-screen bg-gray-50/30">
    <div class="py-4">
      <div class="max-w-4xl mx-auto px-4">
        <!-- 页面标题 -->
        <div class="flex items-center space-x-2 text-gray-900 mb-4">
          <div class="p-1.5 bg-[#fb7299]/5 rounded-lg">
            <svg class="w-6 h-6 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            </svg>
          </div>
          <h1 class="text-2xl font-medium bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">设置</h1>
        </div>

        <!-- 设置列表 -->
        <div class="space-y-4">
          <!-- 基础设置 -->
          <section>
            <h2 class="text-lg font-medium text-gray-900 mb-2 flex items-center space-x-2">
              <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
              </svg>
              <span>基础设置</span>
            </h2>

            <div class="bg-white rounded-lg divide-y divide-gray-200">
              <!-- 服务器配置 -->
              <div class="p-2 m-1 transition-colors duration-200 hover:bg-gray-100 rounded-lg">
                <div class="flex items-center justify-between mb-3">
                  <div>
                    <h3 class="text-base font-medium text-gray-900">服务器配置</h3>
                    <p class="text-sm text-gray-500">配置API服务器地址，修改后将自动刷新页面</p>
                  </div>
                </div>
                <div class="flex space-x-2">
                  <input
                    v-model="serverUrl"
                    type="text"
                    class="flex-1 block rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
                    placeholder="例如：http://localhost:8899"
                  />
                  <button
                    @click="resetServerUrl"
                    class="inline-flex items-center px-3 py-2 text-sm font-medium text-[#fb7299] bg-[#fb7299]/5 rounded-lg hover:bg-[#fb7299]/10"
                  >
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  </button>
                  <button
                    @click="saveServerUrl"
                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90"
                  >
                    保存
                  </button>
                </div>
              </div>

              <!-- 图片源设置 -->
              <div class="p-2 m-1 transition-colors duration-200 hover:bg-gray-100 rounded-lg">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-base font-medium text-gray-900">使用本地图片源</h3>
                    <p class="text-sm text-gray-500">选择使用本地图片源或在线图片源，本地图片源适合离线访问</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="useLocalImages" class="sr-only peer" @change="handleImageSourceChange">
                    <div class="w-11 h-6 bg-gray-200 peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#fb7299]"></div>
                  </label>
                </div>
              </div>

              <!-- 邮件配置 -->
              <div class="p-2 m-1 transition-colors duration-200 hover:bg-gray-100 rounded-lg">
                <div class="flex items-center justify-between mb-2">
                  <h3 class="text-base font-medium text-gray-900">邮件配置</h3>
                  <div class="flex space-x-2">
                    <button
                      @click="resetEmailConfig"
                      class="inline-flex items-center px-3 py-2 text-sm font-medium text-[#fb7299] bg-[#fb7299]/5 rounded-lg hover:bg-[#fb7299]/10"
                    >
                      <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      重置
                    </button>
                    <button
                      @click="saveEmailConfig"
                      class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90"
                    >
                      保存
                    </button>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <div class="space-y-3">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">SMTP服务器</label>
                      <input
                        v-model="emailConfig.smtp_server"
                        type="text"
                        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
                        placeholder="smtp.qq.com"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">发件人邮箱</label>
                      <input
                        v-model="emailConfig.sender"
                        type="email"
                        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
                        placeholder="example@qq.com"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">收件人邮箱</label>
                      <input
                        v-model="emailConfig.receiver"
                        type="email"
                        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
                        placeholder="receiver@qq.com"
                      />
                    </div>
                  </div>
                  <div class="space-y-3">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">SMTP端口</label>
                      <input
                        v-model.number="emailConfig.smtp_port"
                        type="number"
                        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
                        placeholder="587"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">邮箱授权码</label>
                      <input
                        v-model="emailConfig.password"
                        type="password"
                        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
                        placeholder="授权码"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- DeepSeek配置 -->
          <section>
            <h2 class="text-lg font-medium text-gray-900 mb-2 flex items-center space-x-2">
              <svg class="w-5 h-5 text-[#4D6BFE]" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M27.501 8.46875C27.249 8.3457 27.1406 8.58008 26.9932 8.69922C26.9434 8.73828 26.9004 8.78906 26.8584 8.83398C26.4902 9.22852 26.0605 9.48633 25.5 9.45508C24.6787 9.41016 23.9785 9.66797 23.3594 10.2969C23.2275 9.52148 22.79 9.05859 22.125 8.76172C21.7764 8.60742 21.4238 8.45312 21.1807 8.11719C21.0098 7.87891 20.9639 7.61328 20.8779 7.35156C20.8242 7.19336 20.7695 7.03125 20.5879 7.00391C20.3906 6.97266 20.3135 7.13867 20.2363 7.27734C19.9258 7.84375 19.8066 8.46875 19.8174 9.10156C19.8447 10.5234 20.4453 11.6562 21.6367 12.4629C21.7725 12.5547 21.8076 12.6484 21.7646 12.7832C21.6836 13.0605 21.5869 13.3301 21.501 13.6074C21.4473 13.7852 21.3662 13.8242 21.1768 13.7461C20.5225 13.4727 19.957 13.0684 19.458 12.5781C18.6104 11.7578 17.8438 10.8516 16.8877 10.1426C16.6631 9.97656 16.4395 9.82227 16.207 9.67578C15.2314 8.72656 16.335 7.94727 16.5898 7.85547C16.8574 7.75977 16.6826 7.42773 15.8193 7.43164C14.957 7.43555 14.167 7.72461 13.1611 8.10938C13.0137 8.16797 12.8594 8.21094 12.7002 8.24414C11.7871 8.07227 10.8389 8.0332 9.84766 8.14453C7.98242 8.35352 6.49219 9.23633 5.39648 10.7441C4.08105 12.5547 3.77148 14.6133 4.15039 16.7617C4.54883 19.0234 5.70215 20.8984 7.47559 22.3633C9.31348 23.8809 11.4307 24.625 13.8457 24.4824C15.3125 24.3984 16.9463 24.2012 18.7881 22.6406C19.2529 22.8711 19.7402 22.9629 20.5498 23.0332C21.1729 23.0918 21.7725 23.002 22.2373 22.9062C22.9648 22.752 22.9141 22.0781 22.6514 21.9531C20.5186 20.959 20.9863 21.3633 20.5605 21.0371C21.6445 19.752 23.2783 18.418 23.917 14.0977C23.9668 13.7539 23.9238 13.5391 23.917 13.2598C23.9131 13.0918 23.9512 13.0254 24.1445 13.0059C24.6787 12.9453 25.1973 12.7988 25.6738 12.5352C27.0557 11.7793 27.6123 10.5391 27.7441 9.05078C27.7637 8.82422 27.7402 8.58789 27.501 8.46875ZM15.46 21.8613C13.3926 20.2344 12.3906 19.6992 11.9766 19.7227C11.5898 19.7441 11.6592 20.1875 11.7441 20.4766C11.833 20.7617 11.9492 20.959 12.1123 21.209C12.2246 21.375 12.3018 21.623 12 21.8066C11.334 22.2207 10.1768 21.668 10.1221 21.6406C8.77539 20.8477 7.64941 19.7988 6.85547 18.3652C6.08984 16.9844 5.64453 15.5039 5.57129 13.9238C5.55176 13.541 5.66406 13.4062 6.04297 13.3379C6.54199 13.2461 7.05762 13.2266 7.55664 13.2988C9.66602 13.6074 11.4619 14.5527 12.9668 16.0469C13.8262 16.9004 14.4766 17.918 15.1465 18.9121C15.8584 19.9688 16.625 20.9746 17.6006 21.7988C17.9443 22.0879 18.2197 22.3086 18.4824 22.4707C17.6895 22.5586 16.3652 22.5781 15.46 21.8613ZM16.4502 15.4805C16.4502 15.3105 16.5859 15.1758 16.7568 15.1758C16.7949 15.1758 16.8301 15.1836 16.8613 15.1953C16.9033 15.2109 16.9424 15.2344 16.9727 15.2695C17.0273 15.3223 17.0586 15.4004 17.0586 15.4805C17.0586 15.6504 16.9229 15.7852 16.7529 15.7852C16.582 15.7852 16.4502 15.6504 16.4502 15.4805ZM19.5273 17.0625C19.3301 17.1426 19.1328 17.2129 18.9434 17.2207C18.6494 17.2344 18.3281 17.1152 18.1533 16.9688C17.8828 16.7422 17.6895 16.6152 17.6074 16.2168C17.5732 16.0469 17.5928 15.7852 17.623 15.6348C17.6934 15.3105 17.6152 15.1035 17.3877 14.9141C17.2012 14.7598 16.9658 14.7188 16.7061 14.7188C16.6094 14.7188 16.5205 14.6758 16.4541 14.6406C16.3457 14.5859 16.2568 14.4512 16.3418 14.2852C16.3691 14.2324 16.501 14.1016 16.5322 14.0781C16.8838 13.877 17.29 13.9434 17.666 14.0938C18.0146 14.2363 18.2773 14.498 18.6562 14.8672C19.0439 15.3145 19.1133 15.4395 19.334 15.7734C19.5078 16.0371 19.667 16.3066 19.7754 16.6152C19.8408 16.8066 19.7559 16.9648 19.5273 17.0625Z" fill="#4D6BFE" />
              </svg>
              <span>DeepSeek配置</span>
            </h2>

            <div class="bg-white rounded-lg divide-y divide-gray-200">
              <!-- DeepSeek API密钥 -->
              <div class="p-2 m-1 transition-colors duration-200 hover:bg-gray-100 rounded-lg">
                <div class="flex items-center justify-between mb-3">
                  <div>
                    <h3 class="text-base font-medium text-gray-900">DeepSeek API密钥</h3>
                    <p class="text-sm text-gray-500">配置DeepSeek API密钥，用于AI摘要生成</p>
                  </div>
                  <!-- API密钥状态显示 -->
                  <div v-if="deepseekApiKeyStatus.is_set" class="flex items-center space-x-1 px-2 py-1 rounded-full text-xs"
                       :class="deepseekApiKeyStatus.is_valid ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'">
                    <svg v-if="deepseekApiKeyStatus.is_valid" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <svg v-else class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <span>{{ deepseekApiKeyStatus.message }}</span>
                  </div>
                </div>
                <div class="flex space-x-2">
                  <input
                    v-model="deepseekApiKey"
                    type="password"
                    class="flex-1 block rounded-md border-gray-300 shadow-sm focus:border-[#4D6BFE] focus:ring-[#4D6BFE] sm:text-sm"
                    :placeholder="deepseekApiKeyStatus.is_valid ? '已配置有效的API密钥，如需更换请输入新的密钥' : '请输入DeepSeek API密钥'"
                  />
                  <button
                    @click="saveDeepSeekApiKey"
                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-[#4D6BFE] rounded-lg hover:bg-[#4D6BFE]/90"
                  >
                    {{ deepseekApiKeyStatus.is_valid ? '更新' : '保存' }}
                  </button>
                </div>
              </div>

              <!-- DeepSeek余额信息 -->
              <div class="p-2 m-1 transition-colors duration-200 hover:bg-gray-100 rounded-lg">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-base font-medium text-gray-900">DeepSeek余额</h3>
                    <p class="text-sm text-gray-500">查询DeepSeek账户余额信息</p>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button
                      @click="refreshDeepSeekBalance"
                      class="inline-flex items-center px-3 py-2 text-sm font-medium text-[#4D6BFE] bg-[#4D6BFE]/5 rounded-lg hover:bg-[#4D6BFE]/10"
                    >
                      <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      刷新
                    </button>
                  </div>
                </div>
                
                <!-- 余额信息显示 -->
                <div v-if="deepseekBalance.is_available" class="mt-3 p-3 bg-[#4D6BFE]/5 rounded-lg">
                  <div v-for="(balance, index) in deepseekBalance.balance_infos" :key="index" class="flex items-center justify-between">
                    <div class="text-sm text-gray-700">
                      <span class="font-medium">{{ balance.currency }}</span> 余额:
                    </div>
                    <div class="text-sm font-medium text-[#4D6BFE]">
                      {{ balance.total_balance }}
                    </div>
                  </div>
                  <div class="mt-2 text-xs text-gray-500">
                    <div v-for="(balance, index) in deepseekBalance.balance_infos" :key="'detail-'+index">
                      <div class="flex justify-between">
                        <span>赠送余额:</span>
                        <span>{{ balance.granted_balance }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span>充值余额:</span>
                        <span>{{ balance.topped_up_balance }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- 未查询或查询失败状态 -->
                <div v-else class="mt-3 p-3 bg-gray-50 rounded-lg text-sm text-gray-500 text-center">
                  {{ deepseekBalanceMessage || '点击刷新按钮查询余额' }}
                </div>
              </div>
            </div>
          </section>

          <!-- AI摘要配置 -->
          <section>
            <h2 class="text-lg font-medium text-gray-900 mb-2 flex items-center space-x-2">
              <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span>AI摘要配置</span>
            </h2>
            <div class="bg-white rounded-lg">
              <SummaryConfig />
            </div>
          </section>

          <!-- 数据管理 -->
          <section>
            <h2 class="text-lg font-medium text-gray-900 mb-2 flex items-center space-x-2">
              <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
              </svg>
              <span>数据管理</span>
            </h2>

            <div class="bg-white rounded-lg divide-y divide-gray-200">
              <!-- 数据导出 -->
              <div class="p-2 m-1 transition-colors duration-200 hover:bg-gray-100 rounded-lg">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-base font-medium text-gray-900">数据导出</h3>
                    <p class="text-sm text-gray-500">导出历史记录数据到Excel文件，支持按年份导出</p>
                  </div>
                  <div class="flex items-center space-x-4">
                    <select
                      v-model="selectedYear"
                      class="block w-32 rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
                    >
                      <option v-for="year in availableYears" :key="year" :value="year">
                        {{ year }}年
                      </option>
                    </select>
                    <button
                      @click="exportAndDownloadExcel"
                      :disabled="isExporting"
                      class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90 disabled:opacity-50"
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

              <!-- 数据库下载 -->
              <div class="p-2 m-1 transition-colors duration-200 hover:bg-gray-100 rounded-lg">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-base font-medium text-gray-900">数据库下载</h3>
                    <p class="text-sm text-gray-500">下载完整的SQLite数据库文件，包含所有历史记录数据</p>
                  </div>
                  <button
                    @click="downloadSqlite"
                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90"
                  >
                    <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    下载SQLite数据库
                  </button>
                </div>
              </div>
            </div>
          </section>

          <!-- 危险操作 -->
          <section>
            <h2 class="text-lg font-medium text-gray-900 mb-2 flex items-center space-x-2">
              <svg class="w-5 h-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <span>危险操作</span>
            </h2>

            <div class="bg-white rounded-lg">
              <div class="p-2 m-1 transition-colors duration-200 hover:bg-red-100 rounded-lg">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-base font-medium text-gray-900">数据库重置</h3>
                    <p class="text-sm text-gray-500">删除现有数据库并重新导入数据（此操作不可逆）</p>
                  </div>
                  <button
                    @click="handleResetDatabase"
                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600"
                  >
                    <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    重置数据库
                  </button>
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
import { ref, onMounted } from 'vue'
import { showDialog, showNotify } from 'vant'
import { getCurrentBaseUrl, setBaseUrl, resetDatabase, getAvailableYears, importSqliteData, exportHistory, downloadExcelFile, downloadDatabase, getEmailConfig, updateEmailConfig, setDeepSeekApiKey, getDeepSeekBalance, checkDeepSeekApiKey } from '../../api/api'
import 'vant/es/dialog/style'
import 'vant/es/notify/style'
import SummaryConfig from './SummaryConfig.vue'

const selectedYear = ref(new Date().getFullYear())
const availableYears = ref([])
const isExporting = ref(false)
const serverUrl = ref('')
const useLocalImages = ref(localStorage.getItem('useLocalImages') === 'true')
const DEFAULT_EMAIL_CONFIG = {
  smtp_server: 'smtp.qq.com',
  smtp_port: 587,
  sender: '',
  password: '',
  receiver: ''
}
const emailConfig = ref({ ...DEFAULT_EMAIL_CONFIG })

// DeepSeek相关状态
const deepseekApiKey = ref('')
const deepseekApiKeyStatus = ref({
  is_set: false,
  is_valid: false,
  message: ''
})
const deepseekBalance = ref({
  is_available: false,
  balance_infos: []
})
const deepseekBalanceMessage = ref('')

// 初始化服务器地址
onMounted(async () => {
  console.log('Settings组件开始挂载')
  try {
    serverUrl.value = getCurrentBaseUrl()
    console.log('当前服务器地址:', serverUrl.value)

    await Promise.all([
      (async () => {
        console.log('开始初始化邮件配置')
        await initEmailConfig()
        console.log('邮件配置初始化完成')
      })(),
      (async () => {
        console.log('开始获取可用年份')
        try {
          const response = await getAvailableYears()
          if (response.data.status === 'success') {
            availableYears.value = response.data.data.sort((a, b) => b - a)
            if (availableYears.value.length > 0) {
              selectedYear.value = availableYears.value[0]
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
          availableYears.value = [new Date().getFullYear()]
        }
      })(),
      (async () => {
        console.log('开始获取DeepSeek配置')
        await checkDeepSeekApiKeyStatus()
        await refreshDeepSeekBalance()
        console.log('DeepSeek配置获取完成')
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
    isExporting.value = true
    showNotify({
      type: 'primary',
      message: '正在导出数据...'
    })

    const response = await exportHistory(selectedYear.value)
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: '导出成功，准备下载...'
      })

      await downloadExcelFile(selectedYear.value)
      showNotify({
        type: 'success',
        message: '下载完成'
      })
    } else {
      throw new Error(response.data.message)
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `操作失败：${error.message}`
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
const DEFAULT_SERVER_URL = 'http://localhost:8899'

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

// 检查DeepSeek API密钥状态
const checkDeepSeekApiKeyStatus = async () => {
  try {
    const response = await checkDeepSeekApiKey()
    deepseekApiKeyStatus.value = response.data
  } catch (error) {
    console.error('检查DeepSeek API密钥状态失败:', error)
    deepseekApiKeyStatus.value = {
      is_set: false,
      is_valid: false,
      message: '检查API密钥状态失败'
    }
  }
}

// 保存DeepSeek API密钥
const saveDeepSeekApiKey = async () => {
  if (!deepseekApiKey.value) {
    showNotify({
      type: 'warning',
      message: 'API密钥不能为空'
    })
    return
  }

  try {
    const response = await setDeepSeekApiKey(deepseekApiKey.value)
    if (response.data.success) {
      showNotify({
        type: 'success',
        message: response.data.message || 'API密钥已保存'
      })
      // 清空输入框
      deepseekApiKey.value = ''
      // 更新API密钥状态和余额信息
      await checkDeepSeekApiKeyStatus()
      await refreshDeepSeekBalance()
    } else {
      throw new Error(response.data.message || 'API密钥保存失败')
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `保存失败：${error.message || '未知错误'}`
    })
  }
}

// 刷新DeepSeek余额
const refreshDeepSeekBalance = async () => {
  try {
    deepseekBalanceMessage.value = '正在查询余额...'
    const response = await getDeepSeekBalance()
    deepseekBalance.value = response.data
    deepseekBalanceMessage.value = ''
  } catch (error) {
    console.error('获取DeepSeek余额失败:', error)
    deepseekBalance.value = { is_available: false }
    deepseekBalanceMessage.value = error.response?.data?.message || '获取余额失败，请检查API密钥是否正确'
  }
}
</script>
