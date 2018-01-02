public class MyList {
	

	private Object[] array;

	private int size;
	
	private int c;
	
	
	public MyList() {

		array = new Object[16];

		size = 0;
		
		c = 2;

	}

	public Object get(int i) {

		validate(i);

		return array[i];
		
	}	
		
	public void arrayInfo () {
		
		System.out.println ("The size is " + getSize () + ". The ArrayLength is " + getArrayLength());

	}
	
	public void listArrayElements () {
		
		for (int i = 0; i <= getSize() - 1; i++) {
				
			System.out.println("The element " + i + " is " + get(i));
		
		}
	}

	private void validate(int i) {

		if (i >= size) {

			throw new RuntimeException();

		}

	}

	public void put(Object a, int i) {

		validate(i);

		array[i] = a;

	}

	public void add(Object a) {

		if (size == array.length) {

			listExp();
		}

		array[size] = a;

		size++;

	}

	public int getSize() {

		return size;

	}
	
	public int getArrayLength() {
		
		int i = array.length;
		
		return i;
	}

	private void listExp() {

		Object[] array1 = new Object[16 * c];

		for (int i = 0; i < size; i++) {

			array1[i] = array[i];

		}

		array = array1;
		
		c++;

	}
	
	public Object deleteElement (int i) {
		
		validate (i);
		
		Object b = array [i];
		
		for (int a = i+1; a < size; a++) {
			
			array [a-1] = array [a];
			 
		}
		
		size = size-1;
		
		if (size % 16 == 0) {
			
			listShrink();
		
		}	
		
		return b;
		
	}
	
	private void listShrink () {
		
		c--;
		
		Object[] array1 = new Object[array.length - 16];

		for (int i = 0; i < size; i++) {

		array1[i] = array[i];

		}

		array = array1;
			
	}
			
			
			
}
		
		

	

