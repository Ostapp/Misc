
public class SLinkedList {
	
	int value;
	
	SLinkedList next;
	
	private SLinkedList [] asd;
	
	
private SLinkedList () {
	
	asd = new SLinkedList [16];
}
	
public void generateSLinkedListObjects(int n) {
		
		// создавать элементы в количестве n и связывать их
		int i;
		
		for (i = 0; i < n; i++) {
			
			asd [i] = new SLinkedList ();
			
			asd [i].value = i;
			
			if (i > 0) {
				
				asd [i-1].next = asd [i];
				
			}
		}
		
	}
	
	public void printValues (int i) {
		
		for (int a = i; a < asd.length-1; a++) {
			
			if (a == 0) {
				
				System.out.println(asd[a].value);
			}
			
			else if (a == asd.length-1) {
				
				System.out.println(asd[asd.length-1].value);
			}
			
			else {
				
				System.out.println(asd[a-1].next.value);
			
			}	
		
	}
		/*
		SLinkedList fst = new SLinkedList ();
		fst.value = 1; 
		
		SLinkedList snd = new SLinkedList ();
		snd.value = 2;		
		
		fst.next = snd;

		SLinkedList trd = new SLinkedList ();
		snd.next = trd;
		trd.value = 3;
		
		*/
		
	}

	public static void main (String... adsf) {
		
		SLinkedList klmn = new SLinkedList();
		
		klmn.generateSLinkedListObjects(15);
		
		klmn.printValues(0);
		
		/*
		SLinkedList fst = new SLinkedList ();
		fst.value = 1; 
		
		SLinkedList snd = new SLinkedList ();
		snd.value = 2;		
		
		fst.next = snd;

		SLinkedList trd = new SLinkedList ();
		snd.next = trd;
		trd.value = 3;		

		System.out.println(fst.value);
		System.out.println(fst.next.value);
		System.out.println(fst.next.next.value);
		System.out.println(snd.next.value);
		
		*/
		
	}
	
	/*
	public void printAll(SLinkedList elem) {
		// распечатать переданный и все последующие элементы (цикл)
	}
	
	*/
}
