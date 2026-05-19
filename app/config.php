<?php 

$conn = mysqli_connect("localhost", "root", "Yue54345", "crawling_db");
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
?>