import java.util.HashMap;
import java.util.Map;

public class LruCache<K, V> {
    private static class Node<K,V> {
        K key;
        V value;

        Node<K, V> prev;
        Node<K, V> next;

        Node(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }

    private final int capacity;
    private final Map<K, Node<K,V>> map = new HashMap<>();
    private final Node<K, V> head = new Node<>(null, null);
    private final Node<K, V> tail = new Node<>(null, null);

    public LruCache(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be > 0");
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    private void remove(Node<K,V> node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void addToEnd(Node<K, V> node) {
        node.prev = tail.prev;
        node.next = tail;
        tail.prev.next = node;
        tail.prev = node;
    }

    public V get(K key) {
        Node<K, V> node = map.get(key);
        if (node == null) return null;

        remove(node);
        addToEnd(node);
        return node.value;
    }

    public void put(K key, V value) {
        Node<K, V> node = map.get(key);

        if(node != null) {
            node.value = value;
            remove(node);
            addToEnd(node);
            return;
        }
        
        Node<K,V> fresh = new Node<>(key, value);
        map.put(key, fresh);
        addToEnd(fresh);

        if(map.size() >  capacity) {
            Node<K,  V> oldest = head.next;
            remove(oldest);
            map.remove(oldest.key);
        }
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("{");
        for (Node<K,V> n = head.next; n != tail; n = n.next) {
            if (sb.length() > 1) sb.append(", ");
            sb.append(n.key).append('=').append(n.value);
        }
        return sb.append('}').toString();
    }

    public static void main(String[] args) {
        LruCache<String, Integer> cache = new LruCache<>(3);

        cache.put("Khobar", 1);
        cache.put("Dammam", 2);
        cache.put("Riyadh", 3);

        System.out.println("After 3 puts: " + cache);

        cache.get("Khobar");
        System.out.println("After get:    " + cache);

        cache.put("Jeddah", 4);
        System.out.println("After Jeddah: " + cache);

        System.out.println("get Dammam:   " + cache.get("Dammam"));

         // Edge 2: put a key that's already on the shelf (cache is full)
        cache.put("Riyadh", 30);
        System.out.println("Update Riyadh: " + cache);

        // Edge 3: a shelf that holds only one book
        LruCache<String, Integer> tiny = new LruCache<>(1);
        tiny.put("A", 1);
        tiny.put("B", 2);
        System.out.println("Capacity 1:   " + tiny);

        // Edge 4: a shelf that holds zero books
        try {
            new LruCache<String, Integer>(0);
        } catch (IllegalArgumentException e) {
            System.out.println("Capacity 0:   " + e.getMessage());
        }
    }
}