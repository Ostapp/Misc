import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class CalcEngine implements ActionListener {

    Calculator parent;

    CalcEngine(Calculator parent) {

        this.parent = parent;
    }

    @Override
    public void actionPerformed(ActionEvent e) {

        String displText = parent.input.getText();

        JButton source = ((JButton)e.getSource());

        String pressed = (source.getText());

        if (source == parent.backspc && displText.length() > 0) {

            parent.input.setText(displText.substring(0, displText.length()-1));
        }
        else if (source == parent.backspc && displText.length() == 0){
            parent.input.setText("");
        }

        else {
            parent.input.setText(displText + pressed);
        }




        /* press num > add text in the textfield >
           press function > save text from the textfield in a1>
           clean the text field > press num > add text... >
           press function > save text in the textfield in a2 >
           a1

         */


    }
}
