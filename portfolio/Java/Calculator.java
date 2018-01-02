import javax.swing.*;
import java.awt.*;

class Calculator {

    JTextField input;
    JButton num0;
    JButton num1;
    JButton num2;
    JButton num3;
    JButton num4;
    JButton num5;
    JButton num6;
    JButton num7;
    JButton num8;
    JButton num9;
    JButton dot;
    JButton multiple;
    JButton plus;
    JButton divide;
    JButton equals;
    JButton minus;
    JButton backspc;

    Calculator () {

        CalcEngine CalcEngine = new CalcEngine(this);

        // call Panel elements

        // create num buttons
                /* buttons Loop
                for (int i = 0; i < 10; i++) {
                    String a = "num" + i;
                    JButton digit = new JButton(a);
                    System.out.println("button " + i +" is " + a);
                }
                */
        num0 = new JButton("0");
        num0.addActionListener(CalcEngine);
        num1 = new JButton("1");
        num1.addActionListener(CalcEngine);
        num2 = new JButton("2");
        num2.addActionListener(CalcEngine);
        num3 = new JButton("3");
        num3.addActionListener(CalcEngine);
        num4 = new JButton("4");
        num4.addActionListener(CalcEngine);
        num5 = new JButton("5");
        num5.addActionListener(CalcEngine);
        num6 = new JButton("6");
        num6.addActionListener(CalcEngine);
        num7 = new JButton("7");
        num7.addActionListener(CalcEngine);
        num8 = new JButton("8");
        num8.addActionListener(CalcEngine);
        num9 = new JButton("9");
        num9.addActionListener(CalcEngine);
        dot = new JButton(".");
        dot.addActionListener(CalcEngine);

        // create function buttons

        minus = new JButton("-");
        minus.addActionListener(CalcEngine);
        plus = new JButton("+");
        plus.addActionListener(CalcEngine);
        equals = new JButton("=");
        equals.addActionListener(CalcEngine);
        multiple = new JButton("X");
        multiple.addActionListener(CalcEngine);
        divide = new JButton("/");
        divide.addActionListener(CalcEngine);

        // create text field and BackSpace

        input = new JTextField(10);
        input.addActionListener(CalcEngine);
        backspc = new JButton("<<<");
        backspc.addActionListener(CalcEngine);

        // creating panel

        JPanel Panel = new JPanel();

        // creating layout

        GridBagLayout gbl = new GridBagLayout();
        GridBagConstraints constr = new GridBagConstraints();
        Panel.setLayout(gbl);

            //constraints
        constr.weightx = 0;
        constr.weighty = 0;
        constr.gridx = 0;
        constr.gridy = 0;
        constr.gridheight = 1;
        constr.gridwidth = 3;

        gbl.setConstraints(input, constr);
        Panel.add(input);

        constr.weightx = 0;
        constr.weighty = 0;
        constr.gridx = 3;
        constr.gridy = 0;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(backspc, constr);
        Panel.add(backspc);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 0;
        constr.gridy = 1;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(divide, constr);
        Panel.add(divide);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 1;
        constr.gridy = 1;
        constr.gridheight = 1;
        constr.gridwidth = 1;


        gbl.setConstraints(num7, constr);
        Panel.add(num7, constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 2;
        constr.gridy = 1;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(num8, constr);
        Panel.add(num8, constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 3;
        constr.gridy = 1;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(num9, constr);
        Panel.add(num9,constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 0;
        constr.gridy = 2;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(multiple, constr);
        Panel.add(multiple,constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 1;
        constr.gridy = 2;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(num4, constr);
        Panel.add(num4,constr);

        constr.weightx = 0;
        constr.weighty = 0;
        constr.gridx = 2;
        constr.gridy = 2;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(num5, constr);
        Panel.add(num5,constr);

        constr.weightx = 0;
        constr.weighty = 0;
        constr.gridx = 3;
        constr.gridy = 2;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(num6, constr);
        Panel.add(num6,constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 0;
        constr.gridy = 3;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(minus, constr);
        Panel.add(minus,constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 1;
        constr.gridy = 3;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(num1, constr);
        Panel.add(num1,constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 2;
        constr.gridy = 3;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(num2, constr);
        Panel.add(num2,constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 3;
        constr.gridy = 3;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(num3, constr);
        Panel.add(num3,constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 0;
        constr.gridy = 4;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(plus, constr);
        Panel.add(plus,constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 1;
        constr.gridy = 4;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(num0, constr);
        Panel.add(num0,constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 2;
        constr.gridy = 4;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(dot, constr);
        Panel.add(dot,constr);

        constr.weightx = 0;
        constr.weighty= 0;
        constr.gridx = 3;
        constr.gridy = 4;
        constr.gridheight = 1;
        constr.gridwidth = 1;

        gbl.setConstraints(equals, constr);
        Panel.add(equals,constr);

        // creating frame
        JFrame frame = new JFrame("Calculator");
        frame.setContentPane(Panel);
        frame.setVisible(true);

        // calculating frame size

        Toolkit kit = Toolkit.getDefaultToolkit();
        Dimension screenSize = kit.getScreenSize();
        int screenWidth = screenSize.width;
        int screenHeight = screenSize.height;

        frame.setSize(screenWidth / 4, screenHeight / 2);
        frame.setLocationByPlatform(true);

    }

    public static void main(String[]args){

        Calculator Calc = new Calculator();








    }

}