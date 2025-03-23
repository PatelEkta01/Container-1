provider "google" {
  project = "kubernetes-assignment-454116"
  region  = "us-central1-a" 
}

resource "google_container_cluster" "gke_cluster" {
  name     = "ekta-gke-cluster"
  location = "us-central1-a"
  remove_default_node_pool = true
  initial_node_count       = 1

  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 10
    disk_type    = "pd-standard"
    image_type   = "COS_CONTAINERD"
  }

  network    = "default"
  subnetwork = "default"
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "ekta-node-pool"
  location   = "us-central1-a"
  cluster    = google_container_cluster.gke_cluster.name
  node_count = 1

  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 10
    disk_type    = "pd-standard"
    image_type   = "COS_CONTAINERD"
    preemptible  = false
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
