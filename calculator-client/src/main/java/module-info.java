module com.tmas282.calculatorclient {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.tmas282.calculatorclient to javafx.fxml;
    exports com.tmas282.calculatorclient;
}