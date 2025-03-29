<template>
  <div class="min-h-screen bg-gray-50/30">
    <div class="py-4">
      <div class="max-w-4xl mx-auto px-4">
        <!-- 设置导航 -->
        <div class="mb-6">
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-6 overflow-x-auto" aria-label="设置选项卡">
              <button
                v-for="(tab, index) in settingTabs"
                :key="index"
                @click="activeTab = tab.key"
                class="py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === tab.key
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              >
                <div class="w-5 h-5" v-html="tab.icon"></div>
                <span>{{ tab.label }}</span>
              </button>
            </nav>
          </div>
        </div>

        <!-- 设置内容 -->
        <div class="space-y-4">
          <!-- 基础设置 -->
          <section v-if="activeTab === 'basic'">
            <div class="bg-white rounded-lg border border-gray-200 divide-y divide-gray-200">
              <!-- 服务器配置 -->
              <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
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
              <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
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
              <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
                <div class="flex items-center justify-between mb-2">
                  <h3 class="text-base font-medium text-gray-900">邮件配置</h3>
                  <div class="flex space-x-2">
                    <button
                      @click="resetEmailConfig"
                      class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-[#fb7299] bg-[#fb7299]/5 rounded-lg hover:bg-[#fb7299]/10"
                    >
                      <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      重置
                    </button>
                    <button
                      @click="saveEmailConfig"
                      class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-white bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90"
                    >
                      保存
                    </button>
                    <button
                      @click="testEmailConfig"
                      class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-white bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90"
                      :disabled="!isEmailConfigComplete"
                    >
                      <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 19v-8.93a2 2 0 01.89-1.664l7-4.666a2 2 0 012.22 0l7 4.666A2 2 0 0121 10.07V19M3 19a2 2 0 002 2h14a2 2 0 002-2M3 19l6.75-4.5M21 19l-6.75-4.5M3 10l6.75 4.5M21 10l-6.75 4.5m0 0l-1.14.76a2 2 0 01-2.22 0l-1.14-.76" />
                      </svg>
                      测试
                    </button>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-3 mt-2">
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

              <!-- 隐私模式 -->
              <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-base font-medium text-gray-900">隐私模式</h3>
                    <p class="text-sm text-gray-500">开启后将模糊显示标题、封面、UP主名称等敏感信息</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="privacyMode" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#fb7299]"></div>
                  </label>
                </div>
              </div>

              <!-- 首页默认布局设置 -->
              <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
                <div class="flex flex-col space-y-2">
                  <div class="flex items-center justify-between mb-1">
                    <div>
                      <h3 class="text-base font-medium text-gray-900">首页默认布局</h3>
                      <p class="text-sm text-gray-500">设置历史记录页面的默认展示方式</p>
                    </div>
                  </div>
                  <div class="flex items-center space-x-6 mt-2">
                    <div
                      class="flex flex-col items-center cursor-pointer p-2 rounded-lg transition-colors duration-200"
                      @click="setDefaultLayout('grid')"
                      :class="defaultLayout === 'grid' ? 'bg-[#fb7299]/5' : 'hover:bg-gray-100'"
                    >
                      <div class="w-28 h-20 border rounded-lg p-2 flex items-center justify-center mb-2"
                           :class="defaultLayout === 'grid' ? 'border-[#fb7299] bg-[#fb7299]/5' : 'border-gray-200 bg-white'">
                        <div class="grid grid-cols-3 gap-1 w-full">
                          <div v-for="i in 6" :key="i"
                               class="aspect-video rounded-sm"
                               :class="defaultLayout === 'grid' ? 'bg-[#fb7299]/20' : 'bg-gray-200'"></div>
                        </div>
                      </div>
                      <div class="text-sm font-medium" :class="defaultLayout === 'grid' ? 'text-[#fb7299]' : 'text-gray-500'">网格视图</div>
                    </div>
                    <div
                      class="flex flex-col items-center cursor-pointer p-2 rounded-lg transition-colors duration-200"
                      @click="setDefaultLayout('list')"
                      :class="defaultLayout === 'list' ? 'bg-[#fb7299]/5' : 'hover:bg-gray-100'"
                    >
                      <div class="w-28 h-20 border rounded-lg p-2 flex flex-col justify-center space-y-1 mb-2"
                           :class="defaultLayout === 'list' ? 'border-[#fb7299] bg-[#fb7299]/5' : 'border-gray-200 bg-white'">
                        <div v-for="i in 4" :key="i"
                             class="flex w-full h-3 space-x-1">
                          <div class="w-1/3 rounded-sm"
                               :class="defaultLayout === 'list' ? 'bg-[#fb7299]/20' : 'bg-gray-200'"></div>
                          <div class="w-2/3 rounded-sm"
                               :class="defaultLayout === 'list' ? 'bg-[#fb7299]/20' : 'bg-gray-200'"></div>
                        </div>
                      </div>
                      <div class="text-sm font-medium" :class="defaultLayout === 'list' ? 'text-[#fb7299]' : 'text-gray-500'">列表视图</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- DeepSeek配置 -->
          <section v-if="activeTab === 'ai'">
            <div class="bg-white rounded-lg border border-gray-200 divide-y divide-gray-200">
              <!-- DeepSeek API密钥 -->
              <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
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
              <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-base font-medium text-gray-900">DeepSeek余额</h3>
                    <p class="text-sm text-gray-500">查询DeepSeek账户余额信息</p>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button
                      @click="refreshDeepSeekBalance"
                      class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-[#4D6BFE] bg-[#4D6BFE]/5 rounded-lg hover:bg-[#4D6BFE]/10"
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

            <!-- AI摘要配置 -->
            <div class="mt-4">
              <div class="bg-white rounded-lg border border-gray-200">
                <div class="p-4">
                  <h3 class="text-base font-medium text-gray-900 mb-2">AI摘要配置</h3>
                  <SummaryConfig />
                </div>
              </div>
            </div>
          </section>

          <!-- 数据管理 -->
          <section v-if="activeTab === 'data'">
            <div class="bg-white rounded-lg border border-gray-200 divide-y divide-gray-200">
              <!-- 数据导出 -->
              <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
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
              <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
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

            <!-- 危险操作 -->
            <div class="mt-4">
              <div class="bg-white rounded-lg border border-gray-200">
                <div class="p-4 transition-colors duration-200 hover:bg-red-50 rounded-lg">
                  <h3 class="text-base font-medium text-gray-900 mb-2">危险操作</h3>
                  <div class="flex items-center justify-between p-2 border border-red-100 rounded-lg bg-red-50">
                    <div>
                      <h4 class="text-sm font-medium text-red-700">数据库重置</h4>
                      <p class="text-xs text-red-600">删除现有数据库并重新导入数据（此操作不可逆）</p>
                    </div>
                    <button
                      @click="handleResetDatabase"
                      class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600"
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { showNotify, showToast } from 'vant'
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
  testEmailConfig as testEmailApi,
  checkDeepSeekApiKey,
  setDeepSeekApiKey,
  getDeepSeekBalance
} from '../../api/api'
import { setBaseUrl, getCurrentBaseUrl } from '../../api/api'
import { usePrivacyStore } from '../../store/privacy'
import { showDialog } from 'vant'
import SummaryConfig from './SummaryConfig.vue'

// 设置选项卡
const settingTabs = [
  {
    key: 'basic',
    label: '基础设置',
    icon: '<svg class="text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" /></svg>'
  },
  {
    key: 'ai',
    label: 'AI与摘要',
    icon: '<svg class="text-[#4D6BFE]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>'
  },
  {
    key: 'data',
    label: '数据管理',
    icon: '<svg class="text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" /></svg>'
  }
]
const activeTab = ref('basic')

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

// 隐私模式
const { isPrivacyMode, setPrivacyMode } = usePrivacyStore()
const privacyMode = ref(isPrivacyMode.value)

// 默认布局设置
const defaultLayout = ref(localStorage.getItem('defaultLayout') || 'grid')

// 设置默认布局
const setDefaultLayout = (layout) => {
  defaultLayout.value = layout
  localStorage.setItem('defaultLayout', layout)
  showNotify({
    type: 'success',
    message: '默认布局已保存'
  })
}

// 监听隐私模式变化
watch(privacyMode, (newVal) => {
  setPrivacyMode(newVal)
})

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
</script>
