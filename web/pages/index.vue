<template lang="pug">
div
  h1 HLA gallery runner
  p This web wil run HLA typing tools: e.g. hisat2,Kourami,bwa-kit
  p
    | The fastq should smaller than 1G, otherwise it'll timeout and fail,
    | you may need to run some preprocessing to extract the HLA-related reads.

  label Read1(xx.fq.gz)
  input.form-control-file(type="file" v-on:change="readFastq($event, 'read1')")
  span {{ status1 ? "Uploaded" : "Wait for upload" }}
  br
  label Read2(xx.fq.gz)
  input.form-control-file(type="file" v-on:change="readFastq($event, 'read2')")
  span {{ status2 ? "Uploaded" : "Wait for upload" }}
  br
  button.btn.btn-primary(type='button' @click="getName") Create Task   
  p {{ ready }}

  h2 Citation
  h3 Kourami
  p Lee, H., & Kingsford, C. Kourami: graph-guided assembly for novel human leukocyte antigen allele discovery. Genome Biology 19(16), 2018
  h3 hisat2
  p Kim, D., Paggi, J.M., Park, C. et al. Graph-based genome alignment and genotyping with HISAT2 and HISAT-genotype. Nat Biotechnol 37, 907–915 (2019).
  h3 bwakit
  p Li H. (2013) Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM. arXiv:1303.3997v2 [q-bio.GN]. (if you use the BWA-MEM algorithm or the fastmap command, or want to cite the whole BWA package)

  h2 This website
  p Author: linnil1
  p Github: <a href="https://github.com/linnil1/hla-on-aws/">https://github.com/linnil1/hla-on-aws</a>

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
