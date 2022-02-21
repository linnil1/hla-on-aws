import config from "#config"

export default async (req, res) => {
  const arr = req.url.split('/')
  const url = config.AWS_API + "/task/" + arr[1] + "/show/" + arr[2]
  const response = await fetch(url, {method: "POST"})
  return response.text()
}

