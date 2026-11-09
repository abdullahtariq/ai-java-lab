import java.util.LinkedHashMap;
import java.util.Map;

public class LruLinkedDemo {
    static class LruCache<K, V> extends LinkedHashMap<K, V> {
        private final int capacity;

        LruCache(int capacity) {
            super(16, 0.75f, true);
            this.capacity = capacity;
        }

        @Override
        protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
            return size() > capacity;
        }
    }


    public static void main (String[] args) {
        LruCache<String, Integer> cache = new LruCache<>(3);

        cache.put("Khobar", 1);
        cache.put("Dammam", 2);
        cache.put("Riyadh", 3);
        System.out.println("After 3 puts: " + cache);

        cache.get("Khobar");
        System.out.println("After get: " + cache);

        cache.put("Jeddah", 4);
        System.out.println("After Jeddah: " + cache);

    }
}