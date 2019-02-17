<?php
    require_once 'DatabaseConn.php';
    header('Content-Type: application/json ');
    class User {
        private $db;
        private $connect;

        function _construct(){
            $this->db = new DB_Connection();
            $this->connect = $this->db->get_connection();
        }

        public function does_link_exist($link){
            $query = "Select link from links where link = '$link' ";
            $result = mysqli_query($this->connection, $query);
            if(mysqli_num_rows($result) > 0){
            //    $json['success'] = 'Finding Profile';
                echo 'Found a Profile';
            }
            else{
                $query = "Insert into links(link,numOtherLinks) values ($link, 0)";
                $inserted = mysqli_query($this->connection, $query);
                if($inserted == 1) {
                    $json['success'] = 'Link was not in system. Will insert now';
                }
                else{
                    $json['error'] = 'something went wrong, could not insert link';
                }
                echo json_encode($json);
                mysqli_close(this->connection);
            }
        }

    }

    $user = new User();
    if (isset($_POST['link'])) {
        $link = $_POST['link'];

        if(!empty($link)){
            $user -> does_link_exist($link);
        }
        else{
            echo json_encode("no input link found");
        }
    }