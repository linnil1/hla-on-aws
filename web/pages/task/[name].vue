<template lang="pug">
div
  h1 Task {{ $route.params.name }}
  p Job status: {{ data.status }}
  button.btn.btn-secondary(@click="refresh")
    i.fas.fa-sync
  div(v-for="(result, method) in data.result")
    h2 {{ method }}
    template(v-for="(v, k) in result")
      div(v-if="k == 'result_file'")
        p {{ k }} : {{ v }}
        button.btn(@click="showFile(v)") {{ show_on_off[v] ? 'Hide' : 'Show' }} origin file
        pre(v-if="show_on_off[v]") {{ tmp_content[v] }}
      table.table.table-striped(v-else-if="k == 'result'")
        thead.thead-light
          tr
            th.col HLA gene
            th.col 1
            th.col 2
        tbody
          tr(v-for="(gene_called, gene_name) in v")
            th(scope="row") {{ gene_name }}
            td {{ gene_called[0] }}
            td {{ gene_called[1] }}
      p(v-else) {{ k }} : {{ v }}
</template>

<script>
export default {
  data() {
    return {
      // data: { status: "Unknown" }
      data: {
        status: "Unknown",
        // change to result_test to result for debugging
        result_test: {
          'hisat': {
            result_file: "test3.hisat.hisat_v3460.txt",
            result: {
              "A": [ "A*11:01:01:01", "A*31:135" ] ,
              "B": [ "B*31:01" ] ,
      }}}},
      tmp_content: {},
      show_on_off: {},
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    refresh() {
      var name = this.$route.params.name
      console.log(name)
      fetch("/api/status/" + name)
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data)
        this.data = data
      })
    },
    showFile(file_name) {
      // toggle on off
      if (file_name in this.tmp_content) {
        this.show_on_off[file_name] = !this.show_on_off[file_name]
        return
      }
      // query data
      var name = this.$route.params.name
      console.log(name)
      fetch("/api/show/" + name + "/" + file_name)
      .then(response => response.text())
      .then(data => {
        console.log(':', data)
        this.tmp_content[file_name] = data
        this.show_on_off[file_name] = true
      })
    }
  },
}

</script>
