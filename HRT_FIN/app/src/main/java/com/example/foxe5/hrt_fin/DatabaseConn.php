<?php
    class DatabaseConn{
        private $conn;
        function_construct(){
        }

        function _construct(){
            include_once dirname(_FILE_).'/Connect.php';
            $this->conn = new mysqli(db_name, db_user, db_pwd, db_host);

            if(mysqli_connect_errno()){
                echo "Failed to connect with database".mysqli_connect_err();
            }
            else{
                echo "Successful connection"
            }
            return $this->conn
        }

        public function get_connection(){
            return $this->conn();
        }
    }
 ?>