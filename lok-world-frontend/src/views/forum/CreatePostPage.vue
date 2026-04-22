<template>
  <div class="create-post-page">
    <van-nav-bar title="发布帖子" fixed placeholder>
      <template #left>
        <van-icon name="close" @click="handleClose" />
      </template>
      <template #right>
        <van-button type="primary" size="small" :loading="submitting" @click="handleSubmit">发布</van-button>
      </template>
    </van-nav-bar>
    
    <div class="form-content">
      <!-- 标题 -->
      <van-field
        v-model="form.title"
        label="标题"
        placeholder="请输入帖子标题"
        maxlength="50"
        show-word-limit
      />
      
      <!-- 内容 -->
      <van-field
        v-model="form.content"
        type="textarea"
        placeholder="分享你的心得..."
        rows="6"
        maxlength="2000"
        show-word-limit
      />
      
      <!-- 图片上传 -->
      <div class="image-upload">
        <van-uploader
          v-model="form.images"
          :max-count="9"
          :after-read="afterRead"
          @delete="deleteImage"
        >
          <div class="upload-btn">
            <van-icon name="photograph" size="24" />
          </div>
        </van-uploader>
      </div>
      
      <!-- 版块选择 -->
      <van-cell title="选择版块" is-link :value="selectedBoardName" @click="showBoardPicker = true" />
      
      <!-- 阵容推荐 -->
      <van-cell title="添加阵容" is-link value="点击添加" @click="showTeamSelector = true" />
      <div v-if="selectedTeam" class="selected-team">
        <TeamCard :team="selectedTeam" />
        <van-icon name="close" class="remove-team" @click="selectedTeam = null" />
      </div>
    </div>
    
    <!-- 版块选择器 -->
    <van-popup v-model:show="showBoardPicker" position="bottom">
      <van-picker
        :columns="boardColumns"
        @confirm="selectBoard"
        @cancel="showBoardPicker = false"
      />
    </van-popup>
    
    <!-- 阵容选择器 -->
    <van-popup v-model:show="showTeamSelector" position="bottom" :style="{ height: '70%' }">
      <div class="team-selector">
        <h3>选择阵容</h3>
        <van-tabs v-model:active="teamTab">
          <van-tab title="我的阵容" name="mine">
            <div v-if="myTeams.length" class="team-list">
              <div
                v-for="team in myTeams"
                :key="team.id"
                class="team-option"
                :class="{ selected: selectedTeam?.id === team.id }"
                @click="selectTeam(team)"
              >
                <TeamCard :team="team" />
              </div>
            </div>
            <van-empty v-else description="暂无阵容" />
          </van-tab>
          <van-tab title="创建新阵容" name="create">
            <TeamEditor @save="handleTeamSave" />
          </van-tab>
        </van-tabs>
      </div>
    </van-popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showConfirmDialog } from 'vant'
import { createPost, getMyTeams, createTeam } from '@/api/forum'
import TeamCard from '@/components/TeamCard.vue'
import TeamEditor from '@/components/TeamEditor.vue'
import type { Team } from '@/api/types'

const router = useRouter()

// 表单数据
const form = ref({
  title: '',
  content: '',
  images: [] as { url: string; file?: File }[],
  board_id: 0
})

const submitting = ref(false)
const showBoardPicker = ref(false)
const showTeamSelector = ref(false)
const teamTab = ref('mine')
const myTeams = ref<Team[]>([])
const selectedTeam = ref<Team | null>(null)

const boards = [
  { id: 1, name: '攻略' },
  { id: 2, name: '讨论' },
  { id: 3, name: '阵容' },
  { id: 4, name: '交易' },
  { id: 5, name: '求助' }
]

const boardColumns = computed(() => boards.map(b => b.name))

const selectedBoardName = computed(() => {
  const board = boards.find(b => b.id === form.value.board_id)
  return board?.name || '请选择'
})

const afterRead = (file: { file: File; url: string }) => {
  // 文件上传处理
  console.log('upload', file)
}

const deleteImage = (file: { url: string }) => {
  form.value.images = form.value.images.filter(img => img.url !== file.url)
}

const selectBoard = ({ selectedOptions }: { selectedOptions: { text: string }[] }) => {
  const name = selectedOptions[0].text
  const board = boards.find(b => b.name === name)
  if (board) {
    form.value.board_id = board.id
  }
  showBoardPicker.value = false
}

const loadMyTeams = async () => {
  try {
    const res: any = await getMyTeams()
    myTeams.value = res.data || []
  } catch (error) {
    console.error('加载阵容失败:', error)
  }
}

const selectTeam = (team: Team) => {
  selectedTeam.value = team
  showTeamSelector.value = false
}

const handleTeamSave = (team: Team) => {
  myTeams.value.push(team)
  selectedTeam.value = team
  showTeamSelector.value = false
  teamTab.value = 'mine'
}

const handleClose = async () => {
  if (form.value.title || form.value.content) {
    await showConfirmDialog({
      title: '确认退出',
      message: '确定要放弃编辑吗？'
    })
  }
  router.back()
}

const handleSubmit = async () => {
  if (!form.value.title.trim()) {
    showToast('请输入标题')
    return
  }
  if (!form.value.content.trim()) {
    showToast('请输入内容')
    return
  }
  
  submitting.value = true
  try {
    const data = {
      title: form.value.title,
      content: form.value.content,
      images: form.value.images.map(img => img.url),
      board_id: form.value.board_id || undefined,
      team_id: selectedTeam.value?.id
    }
    
    await createPost(data)
    showToast('发布成功')
    router.back()
  } catch (error) {
    showToast('发布失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadMyTeams()
})
</script>

<style scoped>
.create-post-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.form-content {
  padding-top: 46px;
}

.image-upload {
  padding: 12px 16px;
  background: #fff;
}

.upload-btn {
  width: 80px;
  height: 80px;
  background: #f5f5f5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.selected-team {
  position: relative;
  margin: 0 16px 16px;
}

.remove-team {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.team-selector {
  padding: 16px;
}

.team-selector h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
}

.team-list {
  padding: 12px 0;
}

.team-option {
  margin-bottom: 12px;
  border: 2px solid transparent;
  border-radius: 8px;
}

.team-option.selected {
  border-color: #FF6B35;
}
</style>
