resource "docker_image" "nginx" {
  name = "nginx:latest"
}

resource "local_file" "test" {
  filename = "hello.txt"
  content = "Terraform is working!"
}

resource "docker_container" "web" {
  image = docker_image.nginx.image_id
  name = "terraform-nginx"

  ports {
    internal = 80
    external = 8080
  }
}