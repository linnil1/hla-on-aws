import config from "#config"

export default async (req, res) => {
  const url = config.AWS_API + "/create"
  const response = await fetch(url, {method: "POST"})
  return response.json()
}

