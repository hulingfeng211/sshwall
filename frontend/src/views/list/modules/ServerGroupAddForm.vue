<script setup lang="js">
export default {
  name: 'ServerGroupAddForm',

  data () {
    return {
      form: this.$form.createForm(this, { name: 'ServerGroupAddForm' })
    }
  },
  methods: {
    onOk () {
      console.log('监听了 modal ok 事件')
      return new Promise(resolve => {
        resolve(true)
      })
    },
    onCancel () {
      console.log('监听了 modal cancel 事件')
      return new Promise(resolve => {
        resolve(true)
      })
    },
    handleSubmit () {
      const { form: { validateFields } } = this
      this.visible = true
      validateFields((errors, values) => {
        if (!errors) {
          console.log('values', values)
        }
      })
    }
  },
  mounted () {

  },
  beforeDestroy () {
  }
}
</script>

<template>

  <a-form @submit="handleSubmit" :form="form">
    <a-form-item>

      <a-input
        v-decorator="['name', { rules: [{ required: true, message: '请输入服务器组名称' }] }]"
        placeholder="请输入服务器组名称"></a-input>

    </a-form-item>
  </a-form>
</template>

<style scoped lang="less">

</style>
