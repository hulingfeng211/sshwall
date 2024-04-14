
<template>
  <page-header-wrapper>
    <a-card :bordered="false">
      <a-row>
        <a-col :sm="8" :xs="24">
          <info title="服务组" :bordered="false" value="4个人组" />
        </a-col>
        <a-col :sm="8" :xs="24">
          <info title="服务组" :bordered="false" value="4个人组" />
        </a-col>
        <a-col :sm="8" :xs="24">
          <info title="服务组" :bordered="false" value="4个人组" />
        </a-col>
      </a-row>
    </a-card>
    <a-card style="margin-top: 24px">
      <div class="operator">
        <a-button type="primary" icon="plus" @click="add">新建</a-button>
      </div>
    </a-card>

  </page-header-wrapper>

</template>
<script setup lang="js">
import AddFrom from '@/views/list/modules/ServerGroupAddForm.vue'
import Info from '@/views/list/components/Info.vue'
const data = []
export default {
  name: 'ServerGroup',
  components: {
      AddFrom,
      Info
    },
  data () {
    return {
      data,
      status: 'all'
    }
  },
  methods: {
    add () {
      this.$dialog(AddFrom, {
        record: {},
        on: {
          ok () {
            // console.log(this.record)
            console.log('ok')
          },
          cancel () {
            console.log('cancel')
          },
          close () {
            console.log('close')
          }
        }
      })
    },
    edit (record) {
      this.$dialog(AddFrom, {
        record,
        on: {
          ok () {
            console.log('ok')
          },
          cancel () {
            console.log('cancel')
          },
          close () {
            console.log('close')
          }
        }
      })
    }

  },
  computed: {

  },
  mounted () {

  },
  created () {
  }
}
</script>
<style scoped lang="less">
@import '~ant-design-vue/lib/style/themes/default.less';
</style>
