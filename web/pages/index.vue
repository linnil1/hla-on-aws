<template lang="pug">
div
  .h1 HLA gallery runner
  label Read1(xx.fq.gz)
  input.form-control-file(type="file" v-on:change="readFastq($event, 'read1')")
  span {{ status1 }}
  br
  label Read2(xx.fq.gz)
  input.form-control-file(type="file" v-on:change="readFastq($event, 'read2')")
  span {{ status2 }}
  br
  button.btn.btn-primary(type='button' @click="getName") Create Task   
  p {{ ready }}
</template>

<script>
export default {
  data() {
    return {
      status1: false,
      status2: false,
      read1: {},
      read2: {},
      name: "",
    }
  },
  computed: {
    ready() {
      if (this.status1 && this.status2) {
        fetch("/api/submit/" + this.name)
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
          this.$router.push("/task/" + this.name); 
        })
        return true
      }
      return false
    }
  },
  methods: {
    getName() {
      fetch("/api/create")
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        this.name = data.name
        this.uploadFastq(data.read1, "read1")
        this.uploadFastq(data.read2, "read2")
      })
    },
    uploadFastq(data, name) {
      // add file
      if (name == 'read1')
        data.fields.file = this.read1
      else if (name == 'read2')
        data.fields.file = this.read2
        
      // json to formdata
      var fields = new FormData()
      for (const [k, v] of Object.entries(data.fields))
        fields.append(k, v)
      console.log(fields)

      // upload it
      fetch(data.url, {
        method: 'POST',
        // body: JSON.stringify(data.fields),
        body: fields,
        headers: {
          'Access-Control-Allow-Origin': "*",
        },
        mode: 'no-cors',
      }).then(rep => {
        console.log(rep)
        if (name == 'read1')
          this.status1 = true
        else if (name == 'read2')
          this.status2 = true
      })
    },
    readFastq(evt, name) {
      console.log(evt, name)
      if (name == 'read1')
        this.read1 = evt.target.files[0]
      else if (name == 'read2')
        this.read2 = evt.target.files[0]
    }
  },
}

</script>
