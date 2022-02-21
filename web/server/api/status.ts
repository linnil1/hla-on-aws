import config from "#config"

export default async (req, res) => {
  const name = req.url.slice(1)
  const url = config.AWS_API + "/task/" + name + "/status"
  const response = await fetch(url, {method: "POST"})
  return response.json()
}

